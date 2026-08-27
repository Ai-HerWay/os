"""Orchestration, and the edit plan a human signs off before anything renders.

The pipeline deliberately stops here. `analyse` produces a ranked set of clips
with the reasoning shown; a person picks one; only then does `build` cut it.
Nothing in this module publishes, schedules or posts.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .beats import Beat, beat_summary, detect_beats, thin_beats
from .captions import render_ass, write_ass
from .clips import Audience, Candidate, WEIGHTS, emphasis_words, find_candidates
from .config import Project, Style, slugify
from .ffmpeg import MediaInfo, probe
from .render import RenderPlan, render
from .silence import Segment, detect_silences, keep_segments, restrict_to, total_kept
from .timeline import Shot, Timeline, build_shots
from .transcript import Transcript, Word


@dataclass
class Analysis:
    """Everything known about a source clip before a cut is chosen."""

    slug: str
    source: Path
    info: MediaInfo
    transcript: Transcript
    silences: list[Segment]
    keeps: list[Segment]
    beats: list[Beat]
    candidates: list[Candidate]
    audience: Audience

    @property
    def stripped_seconds(self) -> float:
        return self.info.duration - total_kept(self.keeps)

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "source": str(self.source),
            "duration": round(self.info.duration, 2),
            "resolution": f"{self.info.width}x{self.info.height}",
            "fps": round(self.info.fps, 2),
            "silence_removed_seconds": round(self.stripped_seconds, 2),
            "kept_seconds": round(total_kept(self.keeps), 2),
            "word_count": len(self.transcript),
            "beats": beat_summary(self.beats),
            "audience_configured": self.audience.configured,
            "candidates": [c.to_dict() for c in self.candidates],
        }


def analyse(
    source: str | Path,
    transcript: Transcript,
    *,
    style: Style,
    audience: Audience | None = None,
    slug: str | None = None,
    clip_limit: int = 5,
) -> Analysis:
    """Probe, strip silence, mark beats and rank the clips worth cutting."""
    source = Path(source)
    info = probe(source)
    edit = style.edit

    silences = detect_silences(
        source,
        threshold_db=edit.silence_db,
        min_duration=edit.silence_min_duration,
        duration=info.duration,
    )
    keeps = keep_segments(silences, info.duration, pad=edit.pad)
    beats = detect_beats(transcript)
    candidates = find_candidates(
        transcript,
        audience=audience,
        min_seconds=edit.clip_min_seconds,
        max_seconds=edit.clip_max_seconds,
        limit=clip_limit,
    )
    return Analysis(
        slug=slug or slugify(source.stem),
        source=source,
        info=info,
        transcript=transcript,
        silences=silences,
        keeps=keeps,
        beats=beats,
        candidates=candidates,
        audience=audience or Audience(),
    )


@dataclass
class Reel:
    """One chosen clip, cut and ready to render."""

    analysis: Analysis
    candidate: Candidate | None
    window: Segment
    keeps: list[Segment]
    shots: list[Shot]
    timeline: Timeline
    highlights: list[Word] = field(default_factory=list)

    @property
    def click_times(self) -> list[float]:
        """Output times of every punch-in, for the click track."""
        return [shot.out_start for shot in self.shots[1:]]


def build(
    analysis: Analysis,
    *,
    style: Style,
    clip: int | None = None,
    window: tuple[float, float] | None = None,
) -> Reel:
    """Turn a chosen candidate (or an explicit window) into a shot list."""
    if window is not None:
        chosen, span = None, Segment(*window)
    elif clip is not None:
        if not analysis.candidates:
            raise ValueError(
                "no candidates were found. The take may be shorter than the "
                "minimum clip length, or the transcript may be empty."
            )
        if not 1 <= clip <= len(analysis.candidates):
            raise ValueError(
                f"clip {clip} does not exist; there are "
                f"{len(analysis.candidates)} candidates"
            )
        chosen = analysis.candidates[clip - 1]
        span = Segment(chosen.start, chosen.end)
    else:
        chosen, span = None, Segment(0.0, analysis.info.duration)

    keeps = restrict_to(analysis.keeps, span)
    if not keeps:
        raise ValueError(
            f"nothing survives the silence cut between {span.start:.1f}s and "
            f"{span.end:.1f}s. Try raising the threshold with --silence-db."
        )

    beats = thin_beats(
        analysis.beats,
        start=span.start,
        end=span.end,
        min_gap=style.edit.beat_min_gap,
        max_gap=style.edit.beat_max_gap,
    )
    shots = build_shots(
        keeps, beats,
        zoom_levels=style.render.zoom_levels,
        glitch_run=style.render.max_consecutive_punches + 1,
    )
    timeline = Timeline([Segment(s.source_start, s.source_end) for s in shots])
    highlights = emphasis_words(analysis.transcript, span.start, span.end)
    return Reel(
        analysis=analysis, candidate=chosen, window=span,
        keeps=keeps, shots=shots, timeline=timeline, highlights=highlights,
    )


def write_captions(reel: Reel, path: str | Path, *, style: Style) -> Path:
    content = render_ass(
        reel.analysis.transcript,
        reel.timeline,
        style=style,
        window=(reel.window.start, reel.window.end),
        highlight=reel.highlights,
    )
    return write_ass(path, content)


def render_reel(
    reel: Reel,
    output: str | Path,
    *,
    style: Style,
    captions: Path | None = None,
    project: Project | None = None,
    burn: bool = True,
    overlay: Path | None = None,
    click_sfx: Path | None = None,
) -> Path:
    plan = RenderPlan(
        source=reel.analysis.source,
        shots=reel.shots,
        output=Path(output),
        style=style,
        captions=captions if burn else None,
        overlay=overlay,
        click_sfx=click_sfx,
        click_times=reel.click_times if click_sfx else None,
        has_audio=reel.analysis.info.has_audio,
    )
    graph = None
    if project is not None:
        graph = project.workdir(reel.analysis.slug) / "graph.filter"
    return render(plan, graph_path=graph)


# --------------------------------------------------------------------------
# The human-readable plan
# --------------------------------------------------------------------------


def _bar(value: float, width: int = 10) -> str:
    filled = int(round(max(0.0, min(1.0, value)) * width))
    return "#" * filled + "." * (width - filled)


def edit_plan_markdown(analysis: Analysis, *, style: Style) -> str:
    """The approval document: what was found, what it scored, and why."""
    info = analysis.info
    lines: list[str] = []
    add = lines.append

    add(f"# Edit plan: {analysis.slug}")
    add("")
    add("Nothing has been rendered or published. Pick a clip, then run "
        "`render`.")
    add("")
    add("## The source")
    add("")
    add("| | |")
    add("|---|---|")
    add(f"| File | `{analysis.source.name}` |")
    add(f"| Length | {info.duration:.1f}s |")
    add(f"| Frame | {info.width}x{info.height} at {info.fps:.0f}fps |")
    add(f"| Words | {len(analysis.transcript)} |")
    add(f"| Silence found | {len(analysis.silences)} gaps, "
        f"{analysis.stripped_seconds:.1f}s |")
    add(f"| After the strip | {total_kept(analysis.keeps):.1f}s |")
    beat_counts = beat_summary(analysis.beats)
    add(f"| Beats marked | {sum(beat_counts.values())} "
        f"({', '.join(f'{k} {v}' for k, v in sorted(beat_counts.items()))}) |")
    add("")

    if not analysis.audience.configured:
        add("> **Audience profile not configured.** Resonance is scored "
            "neutral for every clip, so the ranking below is about craft only, "
            "not about fit. Add an audience file built from "
            "`memory/business-context.md` to make that column mean something.")
        add("")

    add("## The clips worth cutting")
    add("")
    if not analysis.candidates:
        add(f"None found. Every window inside the "
            f"{style.edit.clip_min_seconds:.0f}-{style.edit.clip_max_seconds:.0f}s "
            "band was either too short or ran past a sentence boundary. "
            "Either the take is shorter than the minimum, or it is one long "
            "unbroken sentence. Widen the band or cut by hand with `--window`.")
        add("")
        return "\n".join(lines) + "\n"

    add("Ranked on the six things that can be read straight off the "
        "transcript. Scores are out of 100 and weighted "
        + ", ".join(f"{k} {v}" for k, v in WEIGHTS.items()) + ".")
    add("")
    add("| # | Time | Length | Score | Opens on |")
    add("|---|---|---|---|---|")
    for candidate in analysis.candidates:
        opening = candidate.hook_line[:60].replace("|", "/")
        add(f"| {candidate.rank} | {candidate.start:.1f}-{candidate.end:.1f}s "
            f"| {candidate.duration:.0f}s | **{candidate.total:.0f}** "
            f"| {opening}... |")
    add("")

    for candidate in analysis.candidates:
        add(f"### Clip {candidate.rank} - {candidate.total:.0f}/100")
        add("")
        add(f"**{candidate.start:.1f}s to {candidate.end:.1f}s** "
            f"({candidate.duration:.0f}s, {candidate.word_count} words)")
        add("")
        add(f"- **Opens:** {candidate.hook_line}")
        add(f"- **Closes:** {candidate.closing_line}")
        add("")
        add("| Dimension | | Score | Why |")
        add("|---|---|---|---|")
        for key in WEIGHTS:
            value = candidate.scores[key]
            notes = "; ".join(candidate.notes.get(key, [])) or "-"
            add(f"| {key} | `{_bar(value)}` | {value:.2f} "
                f"| {notes.replace('|', '/')} |")
        add("")
        if candidate.cold_opens:
            add("**Stronger openings available inside this clip.** Moving one "
                "of these to the front is a reorder of her own words, not a "
                "rewrite:")
            add("")
            for option in candidate.cold_opens:
                add(f"- `{option.start:.1f}s` ({option.hook_score:.2f}) "
                    f"\"{option.text}\" - {'; '.join(option.reasons)}")
            add("")
    add("## Next")
    add("")
    add("```")
    add(f"reelkit render {analysis.slug} --clip 1")
    add("```")
    add("")
    add("Watch it on a phone in daylight before anything else. If the words "
        "are hard to read, the size or the shadow is wrong, not the font.")
    return "\n".join(lines) + "\n"


def shotlist_markdown(reel: Reel) -> str:
    """The cut itself, shot by shot, for checking or rebuilding by hand."""
    lines = [f"# Shot list: {reel.analysis.slug}", ""]
    if reel.candidate:
        lines.append(f"Clip {reel.candidate.rank}, "
                     f"{reel.window.start:.1f}s to {reel.window.end:.1f}s of the source.")
    lines += [
        "",
        f"{len(reel.shots)} shots, {reel.timeline.duration:.1f}s on the cut timeline.",
        "",
        "| # | Source in | Source out | Out at | Length | Zoom | Cut on | Card |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for shot in reel.shots:
        lines.append(
            f"| {shot.index + 1} | {shot.source_start:.2f}s | {shot.source_end:.2f}s "
            f"| {shot.out_start:.2f}s | {shot.duration:.2f}s | {shot.zoom:g}x "
            f"| {shot.reason} | {'yes' if shot.wants_card else ''} |"
        )
    lines += ["", "## Highlighted words", ""]
    if reel.highlights:
        for word in reel.highlights:
            out_at = reel.timeline.map_time_clamped(word.start)
            lines.append(f"- `{out_at:.2f}s` **{word.text.upper()}**")
    else:
        lines.append("None picked.")
    cards = [s for s in reel.shots if s.wants_card]
    if cards:
        lines += [
            "", "## Graphic cards",
            "",
            "These shots hold too long or sit in a run of fast cuts. A graphic "
            "card belongs here rather than another punch-in:",
            "",
        ]
        for shot in cards:
            lines.append(f"- `{shot.out_start:.2f}s` to `{shot.out_end:.2f}s`")
    return "\n".join(lines) + "\n"


def save_analysis(analysis: Analysis, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(analysis.to_dict(), indent=2), encoding="utf-8")
    return path

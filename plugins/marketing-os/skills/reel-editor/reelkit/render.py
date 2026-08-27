"""Building the ffmpeg graph that turns a shot list into a finished reel.

One pass, not several. The source is decoded once, split per shot, each shot
trimmed and punched to its own zoom, then concatenated, captioned and encoded.
Rendering through intermediate files would be easier to read and would cost a
generation of quality at every hop, so the graph is built here instead.

The graph is written to a file and passed with `-filter_complex_script`, which
sidesteps both command-line length limits and shell quoting entirely.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import Style
from .ffmpeg import ffmpeg, ffmpeg_bin, run
from .timeline import Shot


def _even(value: float) -> int:
    """Round to an even integer. Odd dimensions break yuv420p encoding."""
    return max(2, int(round(value / 2)) * 2)


def escape_filter_path(path: str | Path) -> str:
    """Escape a path for use inside a filter argument.

    ffmpeg parses `:` as an option separator and `'` as a quote *inside* the
    filter string, so both need escaping on top of anything the shell does.
    """
    text = str(path)
    for char in ("\\", ":", "'", "[", "]", ","):
        text = text.replace(char, "\\" + char)
    return text


@dataclass
class RenderPlan:
    source: Path
    shots: list[Shot]
    output: Path
    style: Style
    captions: Path | None = None
    fonts_dir: Path | None = None
    overlay: Path | None = None
    click_sfx: Path | None = None
    click_times: list[float] | None = None
    click_gain: float = 0.35
    has_audio: bool = True

    @property
    def duration(self) -> float:
        return sum(shot.duration for shot in self.shots)


def build_filtergraph(plan: RenderPlan) -> str:
    """Assemble the whole filter_complex as a single string."""
    style = plan.style
    width, height = style.render.width, style.render.height
    eyeline = style.render.eyeline
    fps = style.render.fps
    shots = plan.shots
    if not shots:
        raise ValueError("nothing to render: the shot list is empty")

    lines: list[str] = []
    count = len(shots)

    # --- video: split, then one chain per shot ---------------------------
    video_labels = [f"v{i}" for i in range(count)]
    lines.append(f"[0:v]split={count}" + "".join(f"[{label}]" for label in video_labels))

    for i, shot in enumerate(shots):
        crop_w = _even(width / shot.zoom)
        crop_h = _even(height / shot.zoom)
        chain = (
            f"[{video_labels[i]}]"
            f"trim=start={shot.source_start:.3f}:end={shot.source_end:.3f},"
            "setpts=PTS-STARTPTS,"
            # Fill the vertical frame from whatever aspect the source is,
            # keeping the eyes on the upper third rather than centring the face.
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height}:(iw-{width})/2:(ih-{height})*{eyeline:g},"
            # Then the punch-in itself.
            f"crop={crop_w}:{crop_h}:(iw-{crop_w})/2:(ih-{crop_h})*{eyeline:g},"
            f"scale={width}:{height},setsar=1,fps={fps}"
            f"[c{i}]"
        )
        lines.append(chain)

    # --- audio: the same split, trimmed to match --------------------------
    if plan.has_audio:
        audio_labels = [f"a{i}" for i in range(count)]
        lines.append(f"[0:a]asplit={count}" + "".join(f"[{lb}]" for lb in audio_labels))
        for i, shot in enumerate(shots):
            lines.append(
                f"[{audio_labels[i]}]"
                f"atrim=start={shot.source_start:.3f}:end={shot.source_end:.3f},"
                "asetpts=PTS-STARTPTS,"
                "aformat=sample_rates=48000:channel_layouts=stereo"
                f"[d{i}]"
            )

    # --- concat -----------------------------------------------------------
    if plan.has_audio:
        pairs = "".join(f"[c{i}][d{i}]" for i in range(count))
        lines.append(f"{pairs}concat=n={count}:v=1:a=1[cv][ca]")
    else:
        pairs = "".join(f"[c{i}]" for i in range(count))
        lines.append(f"{pairs}concat=n={count}:v=1:a=0[cv]")

    video_label = "cv"
    audio_label = "ca" if plan.has_audio else None

    # --- captions ---------------------------------------------------------
    if plan.captions:
        args = f"filename={escape_filter_path(plan.captions)}"
        if plan.fonts_dir:
            args += f":fontsdir={escape_filter_path(plan.fonts_dir)}"
        lines.append(f"[{video_label}]ass={args}[sv]")
        video_label = "sv"

    # --- overlay kit ------------------------------------------------------
    if plan.overlay:
        lines.append(
            f"[1:v]scale={width}:{height}[ovl]"
        )
        lines.append(f"[{video_label}][ovl]overlay=0:0:format=auto[ov]")
        video_label = "ov"

    # --- click sound on each punch ----------------------------------------
    clicks = plan.click_times or []
    if plan.click_sfx and clicks and audio_label:
        sfx_index = 2 if plan.overlay else 1
        labels = [f"s{i}" for i in range(len(clicks))]
        lines.append(
            f"[{sfx_index}:a]asplit={len(clicks)}" + "".join(f"[{lb}]" for lb in labels)
        )
        for i, (label, at) in enumerate(zip(labels, clicks)):
            delay_ms = max(0, int(at * 1000))
            lines.append(
                f"[{label}]adelay={delay_ms}|{delay_ms},"
                f"volume={plan.click_gain:g},"
                "aformat=sample_rates=48000:channel_layouts=stereo"
                f"[k{i}]"
            )
        mix_inputs = f"[{audio_label}]" + "".join(f"[k{i}]" for i in range(len(clicks)))
        lines.append(
            f"{mix_inputs}amix=inputs={len(clicks) + 1}:"
            "duration=first:normalize=0[mx]"
        )
        audio_label = "mx"

    lines.append(f"[{video_label}]null[outv]")
    if audio_label:
        lines.append(f"[{audio_label}]anull[outa]")

    return ";\n".join(lines)


def render(plan: RenderPlan, *, graph_path: str | Path | None = None) -> Path:
    """Run the render and return the output path."""
    plan.output.parent.mkdir(parents=True, exist_ok=True)
    graph = build_filtergraph(plan)

    graph_file = Path(graph_path) if graph_path else plan.output.with_suffix(".filter")
    graph_file.parent.mkdir(parents=True, exist_ok=True)
    graph_file.write_text(graph, encoding="utf-8")

    args: list[str] = ["-i", str(plan.source)]
    if plan.overlay:
        args += ["-i", str(plan.overlay)]
    if plan.click_sfx and plan.click_times:
        args += ["-i", str(plan.click_sfx)]

    args += ["-filter_complex_script", str(graph_file), "-map", "[outv]"]
    if plan.has_audio:
        args += ["-map", "[outa]"]

    render_style = plan.style.render
    args += [
        "-c:v", "libx264",
        "-profile:v", "high",
        "-crf", str(render_style.crf),
        "-preset", render_style.preset,
        "-pix_fmt", "yuv420p",
        "-r", str(render_style.fps),
        "-movflags", "+faststart",
    ]
    if plan.has_audio:
        args += ["-c:a", "aac", "-b:a", render_style.audio_bitrate, "-ar", "48000"]
    args.append(str(plan.output))

    ffmpeg(args)
    return plan.output


def render_cut_only(
    source: str | Path, shots: list[Shot], output: str | Path, style: Style,
) -> Path:
    """The silence-stripped cut with no punch-ins and no captions.

    This is step one of the first session: confirm the cut sounds natural
    before anything is built on top of it.
    """
    flat = [
        Shot(
            index=shot.index, source_start=shot.source_start,
            source_end=shot.source_end, zoom=1.0, out_start=shot.out_start,
        )
        for shot in shots
    ]
    plan = RenderPlan(
        source=Path(source), shots=flat, output=Path(output), style=style,
    )
    return render(plan)

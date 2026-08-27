"""Command line entry point.

Six commands, in the order you actually use them:

    reelkit ingest raw/clip.mp4     transcribe and find the silence
    reelkit plan clip               rank the clips, write the edit plan
    reelkit cut clip                render the silence strip only, nothing else
    reelkit captions clip --clip 1  write the .ass for CapCut
    reelkit render clip --clip 1    the finished reel
    reelkit status                  what is in the project

`plan` never renders and `render` never publishes. The stop between them is
deliberate: a person picks the clip.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .clips import Audience
from .config import Project, Style, slugify
from .ffmpeg import FFmpegFailed, FFmpegNotFound, probe
from .plan import (
    analyse, build, edit_plan_markdown, render_reel, save_analysis,
    shotlist_markdown, write_captions,
)
from .transcribe import TranscriberMissing, load_or_transcribe
from .transcript import Transcript


def _style(args: argparse.Namespace) -> Style:
    style = Style.load(getattr(args, "style", None))
    if getattr(args, "silence_db", None) is not None:
        style.edit.silence_db = args.silence_db
    if getattr(args, "fps", None) is not None:
        style.render.fps = args.fps
    if getattr(args, "font", None):
        style.caption.font = args.font
    return style


def _project(args: argparse.Namespace) -> Project:
    return Project(getattr(args, "project", None) or Path.cwd()).ensure()


def _resolve_source(project: Project, target: str) -> Path:
    """Accept a path, a bare filename, or a slug already ingested."""
    candidate = Path(target)
    if candidate.exists():
        return candidate
    in_raw = project.raw / target
    if in_raw.exists():
        return in_raw
    matches = sorted(
        p for p in project.raw.glob("*")
        if p.is_file() and slugify(p.stem) == slugify(target)
    )
    if matches:
        return matches[0]
    raise SystemExit(
        f"cannot find {target!r}. Put the file in {project.raw}/ or pass a path."
    )


def _load_analysis_inputs(args, project: Project, style: Style):
    source = _resolve_source(project, args.clip_name)
    slug = slugify(source.stem)
    workdir = project.workdir(slug)
    workdir.mkdir(parents=True, exist_ok=True)
    transcript = load_or_transcribe(
        source,
        workdir / "transcript.json",
        transcript_path=getattr(args, "transcript", None),
        force=getattr(args, "retranscribe", False),
        model=getattr(args, "model", "medium.en"),
    )
    audience = Audience.load(getattr(args, "audience", None))
    return source, slug, workdir, transcript, audience


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------


def cmd_ingest(args) -> int:
    project = _project(args)
    style = _style(args)
    source = _resolve_source(project, args.clip_name)
    slug = slugify(source.stem)
    workdir = project.workdir(slug)
    workdir.mkdir(parents=True, exist_ok=True)

    info = probe(source)
    print(f"{source.name}: {info.duration:.1f}s, {info.width}x{info.height}, "
          f"{info.fps:.0f}fps, audio={'yes' if info.has_audio else 'NO'}")
    if not info.has_audio:
        print("  no audio track: this pipeline has nothing to work with.",
              file=sys.stderr)
        return 1
    if not info.is_vertical:
        print("  heads up: the source is landscape. It will be cropped to "
              "1080x1920, so anything at the edges of frame is going to go.")

    transcript = load_or_transcribe(
        source, workdir / "transcript.json",
        transcript_path=args.transcript,
        force=args.retranscribe,
        model=args.model,
    )
    print(f"  transcript: {len(transcript)} words -> "
          f"{workdir / 'transcript.json'}")

    analysis = analyse(source, transcript, style=style, slug=slug,
                       audience=Audience.load(args.audience))
    save_analysis(analysis, workdir / "analysis.json")
    print(f"  silence: {len(analysis.silences)} gaps, "
          f"{analysis.stripped_seconds:.1f}s to strip")
    print(f"  ready. Next: reelkit plan {slug}")
    return 0


def cmd_plan(args) -> int:
    project = _project(args)
    style = _style(args)
    source, slug, workdir, transcript, audience = _load_analysis_inputs(
        args, project, style
    )
    analysis = analyse(source, transcript, style=style, slug=slug,
                       audience=audience, clip_limit=args.limit)
    save_analysis(analysis, workdir / "analysis.json")
    plan_path = workdir / "EDIT-PLAN.md"
    plan_path.write_text(edit_plan_markdown(analysis, style=style), encoding="utf-8")

    print(f"{len(analysis.candidates)} clip(s) found in {source.name}")
    for candidate in analysis.candidates:
        print(f"  {candidate.rank}. {candidate.total:5.1f}/100  "
              f"{candidate.start:6.1f}-{candidate.end:6.1f}s "
              f"({candidate.duration:.0f}s)  {candidate.hook_line[:56]}")
    if not analysis.audience.configured:
        print("  note: no audience profile, resonance scored neutral "
              "(--audience to fix)")
    print(f"\nedit plan: {plan_path}")
    print("Nothing rendered. Pick a clip, then: "
          f"reelkit render {slug} --clip 1")
    return 0


def _build_reel(args, project: Project, style: Style):
    source, slug, workdir, transcript, audience = _load_analysis_inputs(
        args, project, style
    )
    analysis = analyse(source, transcript, style=style, slug=slug,
                       audience=audience)
    window = tuple(args.window) if getattr(args, "window", None) else None
    reel = build(analysis, style=style, clip=getattr(args, "clip", None),
                 window=window)
    return slug, workdir, reel


def cmd_cut(args) -> int:
    """Step one of the first session: does the silence strip sound natural?"""
    project = _project(args)
    style = _style(args)
    slug, workdir, reel = _build_reel(args, project, style)
    output = workdir / "cut.mp4"
    render_reel(reel, output, style=style, captions=None, project=project,
                burn=False)
    kept = reel.timeline.duration
    print(f"cut only, no punch-ins, no captions: {output}")
    print(f"  {reel.window.duration:.1f}s in, {kept:.1f}s out, "
          f"{reel.window.duration - kept:.1f}s of silence removed")
    print("  Listen to it before building anything on top. If the cuts sound "
          "clipped, raise --pad. If nothing was removed, raise --silence-db "
          "towards -26.")
    return 0


def cmd_captions(args) -> int:
    project = _project(args)
    style = _style(args)
    slug, workdir, reel = _build_reel(args, project, style)
    path = write_captions(reel, project.captions / f"{slug}.ass", style=style)
    print(f"captions: {path}")
    print(f"  {len(reel.highlights)} highlighted: "
          f"{', '.join(w.text for w in reel.highlights) or 'none'}")
    print("  Import straight into CapCut, or let `render` burn it in.")
    return 0


def cmd_render(args) -> int:
    project = _project(args)
    style = _style(args)
    slug, workdir, reel = _build_reel(args, project, style)

    captions = write_captions(reel, project.captions / f"{slug}.ass", style=style)
    (workdir / "SHOT-LIST.md").write_text(shotlist_markdown(reel), encoding="utf-8")

    suffix = f"-clip{args.clip}" if args.clip else ""
    output = Path(args.output) if args.output else project.out / f"{slug}{suffix}.mp4"

    overlay = Path(args.overlay) if args.overlay else None
    click = Path(args.click_sfx) if args.click_sfx else None
    for path, label in ((overlay, "overlay"), (click, "click sfx")):
        if path and not path.exists():
            print(f"  {label} {path} not found, carrying on without it",
                  file=sys.stderr)
    overlay = overlay if overlay and overlay.exists() else None
    click = click if click and click.exists() else None

    render_reel(reel, output, style=style, captions=captions, project=project,
                burn=not args.no_burn, overlay=overlay, click_sfx=click)

    print(f"rendered: {output}")
    print(f"  {len(reel.shots)} shots, {reel.timeline.duration:.1f}s, "
          f"{style.render.width}x{style.render.height}")
    print(f"  shot list: {workdir / 'SHOT-LIST.md'}")
    print(f"  captions:  {captions}")
    print("  Nothing has been posted. Watch it on a phone before it goes "
          "anywhere.")
    return 0


def cmd_status(args) -> int:
    project = _project(args)
    raws = sorted(p for p in project.raw.glob("*") if p.is_file())
    if not raws:
        print(f"no footage in {project.raw}/. Drop a file in and run "
              "`reelkit ingest <file>`.")
        return 0
    print(f"{project.root}")
    for source in raws:
        slug = slugify(source.stem)
        workdir = project.workdir(slug)
        marks = []
        if (workdir / "transcript.json").exists():
            marks.append("transcribed")
        if (workdir / "EDIT-PLAN.md").exists():
            marks.append("planned")
        outs = list(project.out.glob(f"{slug}*.mp4"))
        if outs:
            marks.append(f"{len(outs)} rendered")
        print(f"  {source.name:<40} {', '.join(marks) or 'not started'}")
    return 0


# --------------------------------------------------------------------------
# Argument parsing
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reelkit",
        description="Cut unedited talking-head footage into short-form reels.",
    )
    parser.add_argument("--project", help="project root (default: cwd)")
    parser.add_argument("--style", help="path to a style JSON preset")
    parser.add_argument("--font", help="override the caption font family")
    parser.add_argument("--silence-db", type=int,
                        help="silence threshold in dB (default -32; try -26 "
                             "for a noisy room)")
    parser.add_argument("--fps", type=int, help="output frame rate")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p, *, with_clip: bool = False):
        p.add_argument("clip_name", help="file in raw/, a path, or a slug")
        p.add_argument("--transcript", help="use this Whisper JSON instead of "
                                            "transcribing")
        p.add_argument("--audience", help="audience profile JSON")
        p.add_argument("--model", default="medium.en", help="Whisper model")
        p.add_argument("--retranscribe", action="store_true",
                       help="ignore the cached transcript")
        if with_clip:
            p.add_argument("--clip", type=int,
                           help="which ranked candidate to cut")
            p.add_argument("--window", type=float, nargs=2,
                           metavar=("START", "END"),
                           help="cut an explicit source window instead")

    p_ingest = sub.add_parser("ingest", help="transcribe and detect silence")
    add_common(p_ingest)
    p_ingest.set_defaults(func=cmd_ingest)

    p_plan = sub.add_parser("plan", help="rank the clips, write the edit plan")
    add_common(p_plan)
    p_plan.add_argument("--limit", type=int, default=5,
                        help="how many candidates to rank")
    p_plan.set_defaults(func=cmd_plan)

    p_cut = sub.add_parser("cut", help="render the silence strip only")
    add_common(p_cut, with_clip=True)
    p_cut.set_defaults(func=cmd_cut)

    p_caps = sub.add_parser("captions", help="write the .ass caption file")
    add_common(p_caps, with_clip=True)
    p_caps.set_defaults(func=cmd_captions)

    p_render = sub.add_parser("render", help="render the finished reel")
    add_common(p_render, with_clip=True)
    p_render.add_argument("--output", help="output path")
    p_render.add_argument("--no-burn", action="store_true",
                          help="skip burning captions (keeps the .ass)")
    p_render.add_argument("--overlay", help="PNG overlay to composite")
    p_render.add_argument("--click-sfx", help="sound played on each punch-in")
    p_render.set_defaults(func=cmd_render)

    p_status = sub.add_parser("status", help="what is in the project")
    p_status.set_defaults(func=cmd_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except FFmpegNotFound as exc:
        print(f"ffmpeg: {exc}", file=sys.stderr)
        return 2
    except TranscriberMissing as exc:
        print(f"transcription: {exc}", file=sys.stderr)
        return 2
    except FFmpegFailed as exc:
        print(str(exc), file=sys.stderr)
        return 3
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

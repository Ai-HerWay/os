"""Silence detection and the keep-list it produces.

`silencedetect` tells you where the dead air is. What you actually want is the
inverse: the spans worth keeping, each padded with a little room tone so the cut
does not sound clipped. That inversion is the whole job of this module.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .ffmpeg import ffmpeg_bin, run

_START_RE = re.compile(r"silence_start:\s*(-?[\d.]+)")
_END_RE = re.compile(r"silence_end:\s*(-?[\d.]+)")


@dataclass(frozen=True)
class Segment:
    """A span of source time, in seconds."""

    start: float
    end: float

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise ValueError(f"segment ends before it starts: {self.start} -> {self.end}")


def parse_silence_log(text: str, *, duration: float | None = None) -> list[Segment]:
    """Pull silence spans out of ffmpeg's stderr.

    A trailing `silence_start` with no matching `silence_end` means the clip
    ended in silence; it is closed at `duration` when that is known.
    """
    silences: list[Segment] = []
    pending: float | None = None
    for line in text.splitlines():
        start_match = _START_RE.search(line)
        if start_match:
            pending = max(0.0, float(start_match.group(1)))
            continue
        end_match = _END_RE.search(line)
        if end_match and pending is not None:
            end = float(end_match.group(1))
            if end > pending:
                silences.append(Segment(pending, end))
            pending = None
    if pending is not None and duration is not None and duration > pending:
        silences.append(Segment(pending, duration))
    return silences


def detect_silences(
    source: str | Path,
    *,
    threshold_db: int = -32,
    min_duration: float = 0.35,
    duration: float | None = None,
    log_path: str | Path | None = None,
) -> list[Segment]:
    """Run silencedetect over `source` and return the silent spans."""
    args = [
        ffmpeg_bin(), "-hide_banner", "-nostdin",
        "-i", str(source),
        "-af", f"silencedetect=n={threshold_db}dB:d={min_duration}",
        "-f", "null", "-",
    ]
    import subprocess
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    text = proc.stderr or ""
    if log_path:
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        Path(log_path).write_text(text, encoding="utf-8")
    return parse_silence_log(text, duration=duration)


def keep_segments(
    silences: list[Segment],
    duration: float,
    *,
    pad: float = 0.12,
    min_keep: float = 0.20,
) -> list[Segment]:
    """Invert silences into the spans to keep.

    Each silence is shrunk by `pad` at both ends, so every cut keeps that much
    room tone on either side. A silence shorter than twice the pad disappears
    entirely: it was never long enough to be worth cutting.
    """
    if duration <= 0:
        return []
    trimmed: list[Segment] = []
    for silence in silences:
        start = silence.start + pad
        end = silence.end - pad
        if end - start > 1e-6:
            trimmed.append(Segment(max(0.0, start), min(duration, end)))

    keeps: list[Segment] = []
    cursor = 0.0
    for silence in trimmed:
        if silence.start > cursor:
            keeps.append(Segment(cursor, min(silence.start, duration)))
        cursor = max(cursor, silence.end)
    if cursor < duration:
        keeps.append(Segment(cursor, duration))

    return [k for k in keeps if k.duration >= min_keep]


def total_kept(segments: list[Segment]) -> float:
    return sum(s.duration for s in segments)


def restrict_to(segments: list[Segment], window: Segment) -> list[Segment]:
    """Clip a keep-list down to one window of source time.

    Used when a single candidate reel is rendered out of a longer take.
    """
    out: list[Segment] = []
    for seg in segments:
        start = max(seg.start, window.start)
        end = min(seg.end, window.end)
        if end - start > 1e-6:
            out.append(Segment(start, end))
    return out

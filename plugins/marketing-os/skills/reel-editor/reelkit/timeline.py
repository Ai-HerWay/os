"""Source time to output time, and the shot list in between.

Once silence is stripped, nothing lines up any more: a word spoken at 31.4s in
the raw file might land at 24.1s in the cut. Captions, beat marks and sound
cues all have to be moved through that mapping, so it lives in one class and
everything downstream asks it rather than doing its own arithmetic.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

from .beats import Beat
from .silence import Segment


class Timeline:
    """Maps source time onto the timeline that survives the cut."""

    def __init__(self, segments: list[Segment]):
        self.segments = sorted(segments, key=lambda s: s.start)
        self._offsets: list[float] = []
        running = 0.0
        for segment in self.segments:
            self._offsets.append(running)
            running += segment.duration
        self.duration = running

    def __bool__(self) -> bool:
        return bool(self.segments)

    def map_time(self, source_time: float) -> float | None:
        """Where `source_time` ends up after the cut, or None if it was cut out."""
        for segment, offset in zip(self.segments, self._offsets):
            if segment.start <= source_time <= segment.end:
                return offset + (source_time - segment.start)
        return None

    def map_time_clamped(self, source_time: float) -> float:
        """Like `map_time`, but a cut-out moment snaps to the nearest edge.

        Used for caption timings: a word whose start landed a few milliseconds
        inside a trimmed silence should still be shown, not dropped.
        """
        exact = self.map_time(source_time)
        if exact is not None:
            return exact
        if not self.segments:
            return 0.0
        if source_time < self.segments[0].start:
            return 0.0
        for i, segment in enumerate(self.segments):
            if source_time > segment.end:
                continue
            return self._offsets[i]
        return self.duration

    def contains(self, source_time: float) -> bool:
        return self.map_time(source_time) is not None


@dataclass
class Shot:
    """One continuous piece of source footage at one zoom level."""

    index: int
    source_start: float
    source_end: float
    zoom: float
    out_start: float
    reason: str = ""
    wants_card: bool = False

    @property
    def duration(self) -> float:
        return max(0.0, self.source_end - self.source_start)

    @property
    def out_end(self) -> float:
        return self.out_start + self.duration

    def to_dict(self) -> dict:
        data = asdict(self)
        for key in ("source_start", "source_end", "out_start"):
            data[key] = round(getattr(self, key), 3)
        data["duration"] = round(self.duration, 3)
        return data



def _usable_boundaries(
    segment: Segment, cuts: list[float], min_shot: float,
) -> list[float]:
    """Drop cut points that would make a shot too short to read.

    A shot is bounded by the silence cuts on either side, so a piece that is
    too short cannot always be merged backwards - the shot before it may be on
    the far side of a cut. Dropping the boundary instead merges it forwards,
    which works in both directions and never produces a frame that flashes.
    """
    kept = [segment.start]
    for cut in sorted(cuts):
        if cut - kept[-1] >= min_shot:
            kept.append(cut)
    # If the tail is too short, the last cut is the one that has to go.
    while len(kept) > 1 and segment.end - kept[-1] < min_shot:
        kept.pop()
    kept.append(segment.end)
    return kept


def build_shots(
    segments: list[Segment],
    beats: list[Beat],
    *,
    zoom_levels: list[float] | None = None,
    min_shot: float = 0.6,
    glitch_run: int = 3,
    fast_shot: float = 2.0,
) -> list[Shot]:
    """Split the kept footage at every beat and assign the punch-in schedule.

    Zoom alternates through `zoom_levels` so the frame never lands on the same
    size twice running. Where three or more short shots stack up, the run is
    flagged `wants_card`: three punch-ins in a row reads as a glitch, and the
    third wants a graphic instead.
    """
    zoom_levels = zoom_levels or [1.0, 1.12]
    if not zoom_levels:
        raise ValueError("zoom_levels must not be empty")

    cut_times = sorted({b.time for b in beats if b.action == "cut"})
    reason_at = {round(b.time, 3): b.kind for b in beats if b.action == "cut"}
    card_times = sorted(b.time for b in beats if b.action == "card")

    shots: list[Shot] = []
    out_clock = 0.0
    index = 0
    for segment in sorted(segments, key=lambda s: s.start):
        cuts_inside = [t for t in cut_times if segment.start < t < segment.end]
        boundaries = _usable_boundaries(segment, cuts_inside, min_shot)

        for start, end in zip(boundaries, boundaries[1:]):
            shot = Shot(
                index=index,
                source_start=start,
                source_end=end,
                zoom=zoom_levels[index % len(zoom_levels)],
                out_start=out_clock,
                reason=reason_at.get(round(start, 3), "segment-start"),
                wants_card=any(start <= t < end for t in card_times),
            )
            shots.append(shot)
            out_clock += shot.duration
            index += 1

    _flag_glitch_runs(shots, glitch_run=glitch_run, fast_shot=fast_shot)
    _restack(shots)
    return shots


def _flag_glitch_runs(shots: list[Shot], *, glitch_run: int, fast_shot: float) -> None:
    run = 0
    for shot in shots:
        if shot.duration < fast_shot:
            run += 1
            if run >= glitch_run:
                shot.wants_card = True
                run = 0
        else:
            run = 0


def _restack(shots: list[Shot]) -> None:
    """Recompute output start times after any shot was extended."""
    clock = 0.0
    for i, shot in enumerate(shots):
        shot.index = i
        shot.out_start = clock
        clock += shot.duration


def shots_timeline(shots: list[Shot]) -> Timeline:
    """The source-to-output mapping implied by a finished shot list."""
    return Timeline([Segment(s.source_start, s.source_end) for s in shots])

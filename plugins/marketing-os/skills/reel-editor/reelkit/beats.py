"""Beat marks: where the meaning turns, and therefore where the frame changes.

A beat is not a rhythm in the music sense. It is a point in the speech where
the listener's attention naturally resets - a number lands, a name is used, the
sentence pivots on 'but', or a thought finishes and she breathes. Cutting on
those points feels motivated. Cutting on a metronome feels like a slideshow.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

from .lexicon import PIVOTS, PIVOT_PHRASES, is_number, is_proper_noun, normalise
from .transcript import Transcript

# What each kind of beat is worth when the list has to be thinned.
STRENGTH = {
    "sentence-end": 1.0,
    "number": 0.9,
    "pivot-phrase": 0.85,
    "pivot": 0.7,
    "proper-noun": 0.6,
    "filler": 0.2,
}


@dataclass
class Beat:
    time: float
    kind: str
    word: str
    strength: float
    # 'cut' means punch the frame here. 'card' means the gap to the previous
    # beat was too long to hold on one frame, so a graphic belongs here
    # instead of an extra cut.
    action: str = "cut"

    def to_dict(self) -> dict:
        data = asdict(self)
        data["time"] = round(self.time, 3)
        return data


def detect_beats(transcript: Transcript, *, pause_threshold: float = 0.5) -> list[Beat]:
    """Every candidate beat in the take, before thinning."""
    beats: list[Beat] = []
    starts = set(transcript.sentence_starts())

    for i, word in enumerate(transcript.words):
        clean = word.clean
        if not clean:
            continue

        if is_number(word.text):
            beats.append(Beat(word.start, "number", word.text, STRENGTH["number"]))
            continue

        if clean in PIVOTS:
            # A pivot is only a beat when it turns the sentence, which means it
            # is not the very first word of the take.
            if i > 0:
                beats.append(Beat(word.start, "pivot", word.text, STRENGTH["pivot"]))
            continue

        if is_proper_noun(word.text, is_sentence_start=i in starts):
            beats.append(Beat(
                word.start, "proper-noun", word.text, STRENGTH["proper-noun"]
            ))
            continue

    # Multi-word pivots, matched over a small rolling window.
    for i in range(len(transcript.words)):
        window = " ".join(w.text for w in transcript.words[i:i + 5])
        padded = normalise(window)
        for phrase in PIVOT_PHRASES:
            if padded.startswith(f" {phrase} "):
                beats.append(Beat(
                    transcript.words[i].start, "pivot-phrase", phrase,
                    STRENGTH["pivot-phrase"],
                ))
                break

    # A finished sentence followed by a real breath is the strongest beat there is.
    for i, word in enumerate(transcript.words):
        if word.ends_sentence and transcript.gap_after(i) >= pause_threshold:
            beats.append(Beat(
                word.end, "sentence-end", word.text, STRENGTH["sentence-end"]
            ))

    beats.sort(key=lambda b: (b.time, -b.strength))
    return _dedupe(beats)


def _dedupe(beats: list[Beat], *, window: float = 0.15) -> list[Beat]:
    """Collapse beats landing on effectively the same moment, strongest wins."""
    out: list[Beat] = []
    for beat in beats:
        if out and beat.time - out[-1].time < window:
            if beat.strength > out[-1].strength:
                out[-1] = beat
            continue
        out.append(beat)
    return out


def thin_beats(
    beats: list[Beat],
    *,
    start: float,
    end: float,
    min_gap: float = 2.0,
    max_gap: float = 3.0,
) -> list[Beat]:
    """Reduce the beat list to one frame change every `min_gap` to `max_gap`.

    Two rules, both from the design system: where beats crowd, the weakest are
    dropped rather than cut through; where they thin out, the hold is marked
    for a graphic card rather than filled with an invented cut.
    """
    inside = [b for b in beats if start <= b.time < end]
    inside.sort(key=lambda b: b.time)

    kept: list[Beat] = []
    for beat in inside:
        if not kept:
            kept.append(beat)
            continue
        gap = beat.time - kept[-1].time
        if gap >= min_gap:
            kept.append(beat)
        elif beat.strength > kept[-1].strength and len(kept) > 1:
            # Swap in the stronger beat only if doing so keeps the spacing legal.
            if beat.time - kept[-2].time >= min_gap:
                kept[-1] = beat

    # A hold only wants a card once it is clearly longer than the target,
    # not when it merely overshoots by a fraction of a second. Sitting on one
    # frame for three and a bit seconds is fine; sitting for five is a stall.
    card_threshold = max_gap * 1.5

    def _cards_across(gap_start: float, gap_end: float) -> list[Beat]:
        gap = gap_end - gap_start
        if gap <= card_threshold:
            return []
        count = max(1, int(gap // max_gap) - 1)
        step = gap / (count + 1)
        return [
            Beat(gap_start + step * (n + 1), "hold", "", 0.0, action="card")
            for n in range(count)
        ]

    if not kept:
        # Nothing in this stretch turns: no numbers, no pivots, no finished
        # sentence with a breath after it. Rather than inventing cuts, mark
        # the whole span for graphic cards and let the editor decide.
        return _cards_across(start, end)

    filled: list[Beat] = []
    for beat in kept:
        if filled:
            filled.extend(_cards_across(filled[-1].time, beat.time))
        filled.append(beat)

    filled.extend(_cards_across(filled[-1].time, end))
    return filled


def beat_summary(beats: list[Beat]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for beat in beats:
        counts[beat.kind] = counts.get(beat.kind, 0) + 1
    return counts

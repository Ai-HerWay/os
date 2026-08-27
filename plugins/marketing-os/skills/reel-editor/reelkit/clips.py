"""Choosing which 30 seconds of a long take is worth posting.

This is the judgement half of the pipeline, and it is deliberately built out of
features you can read off the transcript and check by hand: how the opening line
is built, whether the ending resolves, how much filler is in it, how densely it
touches what the audience actually came for.

It ranks her own words. It never writes new ones, and it never claims a clip
will perform - only that it has more of the properties that tend to hold
attention than the clip beside it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

from .lexicon import (
    EMPHASIS_MARKERS, FILLERS, FILLER_PHRASES, HOOK_MARKERS, STOPWORDS,
    HARD_FILLERS, PAYOFF_MARKERS, PIVOT_PHRASES, WEAK_OPENERS,
    contains_phrase, count_phrases, is_number, matched_phrase,
)
from .transcript import Transcript, Word

# What each dimension is worth. They sum to 100 so a score reads as a percentage.
WEIGHTS = {
    "hook": 30,
    "resonance": 20,
    "cleanliness": 15,
    "payoff": 15,
    "pace": 10,
    "shape": 10,
}


# --------------------------------------------------------------------------
# Audience
# --------------------------------------------------------------------------


@dataclass
class Audience:
    """Who this is for, in the only terms a script can check: her words.

    Built from `memory/business-context.md` rather than guessed. When it is
    absent, resonance scores neutral and says so, instead of pretending.
    """

    name: str = ""
    keywords: list[str] = field(default_factory=list)
    pain_points: list[str] = field(default_factory=list)
    avoid: list[str] = field(default_factory=list)

    @property
    def configured(self) -> bool:
        return bool(self.keywords or self.pain_points)

    @classmethod
    def load(cls, path: str | Path | None) -> "Audience":
        if not path:
            return cls()
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            name=data.get("name", ""),
            keywords=[k.lower() for k in data.get("keywords", [])],
            pain_points=[p.lower() for p in data.get("pain_points", [])],
            avoid=[a.lower() for a in data.get("avoid", [])],
        )


# --------------------------------------------------------------------------
# Sentences
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Sentence:
    index: int
    first_word: int
    last_word: int
    start: float
    end: float
    text: str

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)


def sentences(transcript: Transcript) -> list[Sentence]:
    """Split the transcript on terminal punctuation."""
    result: list[Sentence] = []
    first = 0
    for i, word in enumerate(transcript.words):
        is_last = i == len(transcript.words) - 1
        if word.ends_sentence or is_last:
            chunk = transcript.words[first:i + 1]
            if chunk:
                result.append(Sentence(
                    index=len(result),
                    first_word=first,
                    last_word=i,
                    start=chunk[0].start,
                    end=chunk[-1].end,
                    text=" ".join(w.text.strip() for w in chunk).strip(),
                ))
            first = i + 1
    return result


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def score_hook(line: str) -> tuple[float, list[str]]:
    """How hard the opening line works, from 0 to 1.

    Everything rewarded here is a property of the sentence itself: who it
    addresses, whether it carries a concrete number, whether it opens tension,
    and whether it gets to the point before attention is gone.
    """
    notes: list[str] = []
    words = line.split()
    if not words:
        return 0.0, ["empty opening line"]

    lowered = line.lower().strip()
    score = 0.35  # a sentence that merely starts cleanly

    if lowered.rstrip().endswith("?"):
        score += 0.18
        notes.append("opens on a question")

    tokens = {w.strip(".,!?;:\"')(").lower() for w in words}
    hits = tokens & HOOK_MARKERS
    if hits:
        score += min(0.20, 0.07 * len(hits))
        notes.append("tension or direct address: " + ", ".join(sorted(hits)[:3]))

    if any(is_number(w) for w in words):
        score += 0.15
        notes.append("carries a concrete number")

    pivot = matched_phrase(line, PIVOT_PHRASES)
    if pivot:
        score += 0.12
        notes.append(f"opens on a spoken pivot: {pivot!r}")

    if len(words) <= 12:
        score += 0.12
        notes.append(f"short opener ({len(words)} words)")
    elif len(words) > 24:
        score -= 0.15
        notes.append(f"opener runs long ({len(words)} words)")

    for weak in WEAK_OPENERS:
        if lowered.startswith(weak + " ") or lowered == weak:
            score -= 0.25
            notes.append(f"starts on a warm-up word: {weak!r}")
            break

    filler_count = len([w for w in tokens if w in HARD_FILLERS])
    if filler_count:
        score -= 0.08 * filler_count
        notes.append(f"{filler_count} filler word(s) in the opener")

    return _clamp(score), notes


def score_payoff(line: str, *, resolves: bool) -> tuple[float, list[str]]:
    notes: list[str] = []
    score = 0.3
    if resolves:
        score += 0.25
        notes.append("ends on a finished sentence")
    else:
        notes.append("ends mid-sentence, will need a manual trim")

    tokens = {w.strip(".,!?;:\"')(").lower() for w in line.split()}
    hits = tokens & PAYOFF_MARKERS
    if hits:
        score += min(0.30, 0.10 * len(hits))
        notes.append("lands a conclusion: " + ", ".join(sorted(hits)[:3]))
    if any(is_number(w) for w in line.split()):
        score += 0.10
        notes.append("closes on a number")
    if len(line.split()) < 4:
        score -= 0.15
        notes.append("closing line is very short")
    return _clamp(score), notes


def score_pace(words_per_second: float) -> tuple[float, list[str]]:
    """Conversational delivery sits near 2.3-3.6 words a second."""
    if words_per_second <= 0:
        return 0.0, ["no speech detected"]
    low, high = 2.3, 3.6
    if low <= words_per_second <= high:
        return 1.0, [f"pace {words_per_second:.1f} words/sec, in the band"]
    if words_per_second < low:
        score = _clamp(words_per_second / low)
        return score, [f"pace {words_per_second:.1f} words/sec, slow for short form"]
    score = _clamp(1.0 - (words_per_second - high) / 2.0)
    return score, [f"pace {words_per_second:.1f} words/sec, fast, captions will lag"]


def score_cleanliness(
    words: list[Word], text: str, duration: float,
) -> tuple[float, list[str]]:
    """Penalise filler density and dead air inside the window."""
    notes: list[str] = []
    if not words:
        return 0.0, ["no words in window"]

    fillers = len([w for w in words if w.clean in FILLERS])
    fillers += count_phrases(text, FILLER_PHRASES)
    filler_ratio = fillers / len(words)
    filler_score = _clamp(1.0 - filler_ratio * 8)
    if fillers:
        notes.append(f"{fillers} filler(s), {filler_ratio:.0%} of words")
    else:
        notes.append("no filler detected")

    spoken = sum(w.duration for w in words)
    dead_ratio = _clamp(1.0 - spoken / duration) if duration > 0 else 1.0
    dead_score = _clamp(1.0 - max(0.0, dead_ratio - 0.25) * 2.5)
    if dead_ratio > 0.35:
        notes.append(f"{dead_ratio:.0%} dead air before the silence cut")

    return (filler_score * 0.6 + dead_score * 0.4), notes


def score_resonance(text: str, audience: Audience) -> tuple[float, list[str]]:
    """How much of what the audience came for this clip actually touches."""
    if not audience.configured:
        return 0.5, [
            "no audience profile configured, resonance scored neutral "
            "(add one from memory/business-context.md to make this real)"
        ]
    lowered = f" {text.lower()} "
    hit_keywords = [k for k in audience.keywords if f" {k} " in lowered or k in lowered]
    hit_pains = [p for p in audience.pain_points if p in lowered]
    avoided = [a for a in audience.avoid if a in lowered]

    notes: list[str] = []
    score = 0.15
    if hit_pains:
        score += min(0.50, 0.18 * len(hit_pains))
        notes.append("names a stated pain point: " + ", ".join(hit_pains[:3]))
    if hit_keywords:
        score += min(0.35, 0.09 * len(hit_keywords))
        notes.append("audience language: " + ", ".join(hit_keywords[:4]))
    if not hit_pains and not hit_keywords:
        notes.append("touches nothing in the audience profile")
    if avoided:
        score -= 0.30
        notes.append("contains flagged language: " + ", ".join(avoided[:3]))
    return _clamp(score), notes


def score_shape(
    duration: float, *, starts_clean: bool, min_s: float, max_s: float,
) -> tuple[float, list[str]]:
    notes: list[str] = []
    score = 0.0
    sweet_low, sweet_high = min_s + 5, max_s - 8
    if sweet_low <= duration <= sweet_high:
        score += 0.7
        notes.append(f"{duration:.0f}s, in the sweet spot")
    elif min_s <= duration <= max_s:
        score += 0.45
        notes.append(f"{duration:.0f}s, inside the band")
    else:
        notes.append(f"{duration:.0f}s, outside the target band")
    if starts_clean:
        score += 0.3
        notes.append("starts on a sentence boundary")
    else:
        notes.append("starts mid-sentence")
    return _clamp(score), notes


# --------------------------------------------------------------------------
# Candidates
# --------------------------------------------------------------------------


@dataclass
class ColdOpen:
    """A line from later in the clip strong enough to lift to the front.

    A cold open is a reorder, never a rewrite: the words are hers, moved.
    """

    text: str
    start: float
    end: float
    hook_score: float
    reasons: list[str]


@dataclass
class Candidate:
    rank: int
    start: float
    end: float
    text: str
    hook_line: str
    closing_line: str
    scores: dict[str, float]
    total: float
    notes: dict[str, list[str]]
    word_count: int
    cold_opens: list[ColdOpen] = field(default_factory=list)

    @property
    def duration(self) -> float:
        return self.end - self.start

    def to_dict(self) -> dict:
        data = asdict(self)
        data["duration"] = round(self.duration, 2)
        data["start"] = round(self.start, 3)
        data["end"] = round(self.end, 3)
        data["total"] = round(self.total, 1)
        data["scores"] = {k: round(v, 3) for k, v in self.scores.items()}
        return data


def _overlap(a: Candidate, b: Candidate) -> float:
    inner = min(a.end, b.end) - max(a.start, b.start)
    if inner <= 0:
        return 0.0
    return inner / min(a.duration, b.duration)


def find_candidates(
    transcript: Transcript,
    *,
    audience: Audience | None = None,
    min_seconds: float = 20.0,
    max_seconds: float = 45.0,
    limit: int = 5,
    overlap_threshold: float = 0.5,
) -> list[Candidate]:
    """Rank every sentence-aligned window inside the length band.

    Windows are built from sentence boundaries so a clip never opens or closes
    mid-thought, then suppressed against each other so the returned list is
    genuinely different clips rather than five shifts of the same one.
    """
    audience = audience or Audience()
    sents = sentences(transcript)
    if not sents:
        return []

    scored: list[Candidate] = []
    for i, first in enumerate(sents):
        for j in range(i, len(sents)):
            last = sents[j]
            duration = last.end - first.start
            if duration < min_seconds:
                continue
            if duration > max_seconds:
                break

            words = transcript.words[first.first_word:last.last_word + 1]
            text = " ".join(w.text.strip() for w in words).strip()
            if not words:
                continue

            hook, hook_notes = score_hook(first.text)
            payoff, payoff_notes = score_payoff(
                last.text, resolves=transcript.words[last.last_word].ends_sentence
            )
            pace, pace_notes = score_pace(len(words) / duration if duration else 0)
            clean, clean_notes = score_cleanliness(words, text, duration)
            resonance, resonance_notes = score_resonance(text, audience)
            shape, shape_notes = score_shape(
                duration, starts_clean=True, min_s=min_seconds, max_s=max_seconds
            )

            parts = {
                "hook": hook, "resonance": resonance, "cleanliness": clean,
                "payoff": payoff, "pace": pace, "shape": shape,
            }
            total = sum(parts[k] * WEIGHTS[k] for k in WEIGHTS)

            scored.append(Candidate(
                rank=0,
                start=first.start,
                end=last.end,
                text=text,
                hook_line=first.text,
                closing_line=last.text,
                scores=parts,
                total=total,
                notes={
                    "hook": hook_notes, "payoff": payoff_notes,
                    "pace": pace_notes, "cleanliness": clean_notes,
                    "resonance": resonance_notes, "shape": shape_notes,
                },
                word_count=len(words),
            ))

    scored.sort(key=lambda c: c.total, reverse=True)

    chosen: list[Candidate] = []
    for candidate in scored:
        if any(_overlap(candidate, kept) > overlap_threshold for kept in chosen):
            continue
        chosen.append(candidate)
        if len(chosen) >= limit:
            break

    for position, candidate in enumerate(chosen, start=1):
        candidate.rank = position
        candidate.cold_opens = find_cold_opens(transcript, candidate)
    return chosen


def find_cold_opens(
    transcript: Transcript, candidate: Candidate, *, limit: int = 3,
) -> list[ColdOpen]:
    """Lines inside the clip that would hook harder than the one it opens on."""
    opens: list[ColdOpen] = []
    current, _ = score_hook(candidate.hook_line)
    for sentence in sentences(transcript):
        if sentence.start < candidate.start or sentence.end > candidate.end:
            continue
        if sentence.text.strip() == candidate.hook_line.strip():
            continue
        score, reasons = score_hook(sentence.text)
        if score <= current + 0.05:
            continue
        opens.append(ColdOpen(
            text=sentence.text,
            start=sentence.start,
            end=sentence.end,
            hook_score=round(score, 3),
            reasons=reasons,
        ))
    opens.sort(key=lambda o: o.hook_score, reverse=True)
    return opens[:limit]


def emphasis_words(
    transcript: Transcript, start: float, end: float, *, limit: int = 5,
) -> list[Word]:
    """Pick the 3 to 5 words worth highlighting in the captions.

    Numbers first, then the emphasis lexicon, then the longest content words,
    spaced out so two highlights never land back to back.
    """
    window = transcript.words_between(start, end)
    ranked: list[tuple[float, Word]] = []
    for word in window:
        clean = word.clean
        if len(clean) < 4 or clean in STOPWORDS or clean in FILLERS:
            continue
        weight = 0.0
        if is_number(word.text):
            weight = 3.0
        elif clean in EMPHASIS_MARKERS:
            weight = 2.2
        elif len(clean) >= 7:
            weight = 1.0 + min(0.9, len(clean) / 20)
        if weight:
            ranked.append((weight, word))

    ranked.sort(key=lambda pair: pair[0], reverse=True)
    picked: list[Word] = []
    min_gap = max(1.5, (end - start) / (limit * 2))
    for _, word in ranked:
        if len(picked) >= limit:
            break
        if any(abs(word.start - other.start) < min_gap for other in picked):
            continue
        picked.append(word)
    picked.sort(key=lambda w: w.start)
    return picked

"""Word lists the editor reasons with.

These are deliberately small, readable and editable. They encode what makes a
spoken line land, not what makes it true: nothing here invents content, it only
decides which of the words she already said get the emphasis.
"""

from __future__ import annotations

import re

# Words that signal the meaning is turning. These are the beat marks.
PIVOTS = {
    "but", "so", "actually", "however", "instead", "because", "though",
    "until", "unless", "yet", "except", "otherwise", "meanwhile", "still",
}

# Multi-word pivots, matched against the running text.
PIVOT_PHRASES = (
    "the thing is", "here is the thing", "here's the thing", "the truth is",
    "what actually happened", "and that is when", "and that's when",
    "which means", "the problem is", "the real question",
)

# Openers that stop a scroll: direct address, tension, or a promise.
HOOK_MARKERS = {
    "you", "your", "youre", "stop", "never", "nobody", "everyone", "everybody",
    "why", "how", "what", "most", "nobodys", "worst", "biggest", "truth",
    "mistake", "wrong", "secret", "reason", "actually", "myth",
}

# Openers that lose one. A reel that starts here is starting too slowly.
WEAK_OPENERS = (
    "so", "um", "uh", "okay", "ok", "right", "well", "anyway", "basically",
    "hi", "hey", "hello", "welcome", "today", "in this video", "i just wanted",
    "i want to talk about", "let me tell you a little",
)

# Filler. High density means the take needs a tighter cut, not a longer one.
FILLERS = {
    "um", "uh", "erm", "ah", "er", "hmm", "like", "basically", "literally",
    "obviously", "essentially", "honestly", "sorta", "kinda", "yeah",
}
# Unambiguous filler: these are never a real word choice.
HARD_FILLERS = {"um", "uh", "erm", "ah", "er", "hmm", "sorta", "kinda"}

FILLER_PHRASES = (
    "you know", "sort of", "kind of", "i mean", "or whatever", "and stuff",
    "at the end of the day",
)

# Words that signal the line is landing the point rather than setting it up.
PAYOFF_MARKERS = {
    "so", "therefore", "result", "results", "means", "meant", "lesson",
    "start", "started", "stop", "change", "changed", "difference", "matters",
    "point", "why", "remember", "instead", "now", "today", "finally",
}

# Emphasis candidates for the highlighted captions.
EMPHASIS_MARKERS = HOOK_MARKERS | PAYOFF_MARKERS | {
    "everything", "nothing", "always", "first", "last", "only", "free",
    "hard", "easy", "fast", "slow", "more", "less", "double", "half",
}

# Function words. They can carry a sentence but they never carry a highlight,
# so they are excluded from emphasis regardless of what else matches.
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "at", "for", "with",
    "is", "are", "was", "were", "be", "been", "am", "it", "its", "this", "that",
    "these", "those", "i", "me", "my", "we", "us", "our", "he", "she", "they",
    "them", "his", "her", "their", "you", "your", "what", "who", "when", "then",
    "than", "as", "if", "but", "so", "not", "no", "do", "did", "does", "have",
    "has", "had", "will", "would", "can", "could", "just", "very", "one", "all",
    "get", "got", "up", "out", "about", "into", "from", "by", "there", "here",
}

_NUMBER_RE = re.compile(r"^\$?\d[\d,.]*[%kmx]?$", re.IGNORECASE)
_SPELLED_NUMBERS = {
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "twenty", "thirty", "forty", "fifty",
    "hundred", "thousand", "million", "billion", "half", "double", "triple",
}


def is_number(text: str) -> bool:
    """True for '40', '$2M', '80%', '3x' and for spelled-out numbers."""
    stripped = text.strip().strip(".,!?;:\"')(")
    if not stripped:
        return False
    if _NUMBER_RE.match(stripped):
        return True
    return stripped.lower() in _SPELLED_NUMBERS


def is_proper_noun(text: str, *, is_sentence_start: bool = False) -> bool:
    """Capitalised mid-sentence, which is the only signal a transcript gives.

    Sentence-initial capitals are excluded because every sentence has one.
    """
    stripped = text.strip().strip(".,!?;:\"')(")
    if len(stripped) < 2 or is_sentence_start:
        return False
    return stripped[0].isupper() and not stripped.isupper()


_PUNCT_RE = re.compile(r"[^\w\s']+", re.UNICODE)


def normalise(text: str) -> str:
    """Lowercase, strip punctuation, pad with spaces.

    Phrase matching runs on this so that "The thing is, I built ..." still
    matches "the thing is" - the comma is not allowed to hide the pivot.
    """
    flattened = _PUNCT_RE.sub(" ", text.lower())
    return " " + " ".join(flattened.split()) + " "


def contains_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    padded = normalise(text)
    return any(f" {phrase} " in padded for phrase in phrases)


def matched_phrase(text: str, phrases: tuple[str, ...]) -> str | None:
    """The first phrase from `phrases` present in `text`, or None."""
    padded = normalise(text)
    for phrase in phrases:
        if f" {phrase} " in padded:
            return phrase
    return None


def count_phrases(text: str, phrases: tuple[str, ...]) -> int:
    padded = normalise(text)
    return sum(padded.count(f" {phrase} ") for phrase in phrases)

"""Fixtures shared by the tests.

`build_transcript` fakes plausible word timings from plain text so the pure
logic can be exercised without a media file or a Whisper model.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reelkit.transcript import Transcript, Word  # noqa: E402


def build_transcript(
    text: str, *, start: float = 0.0, words_per_second: float = 2.8,
    sentence_pause: float = 0.6,
) -> Transcript:
    """Lay `text` out on a timeline at a steady speaking rate."""
    step = 1.0 / words_per_second
    words: list[Word] = []
    clock = start
    for token in text.split():
        end = clock + step * 0.82
        words.append(Word(text=token, start=round(clock, 3), end=round(end, 3)))
        clock = end + step * 0.18
        if token.rstrip("\"')]").endswith((".", "!", "?")):
            clock += sentence_pause
    return Transcript(words=words, language="en", source="fixture")


# A talking-head take with a slow warm-up, a strong middle, and a weak tail.
SAMPLE_TAKE = (
    "So um I just wanted to jump on here today and talk a little bit about "
    "something that has been on my mind for a while now. "
    "Most women founders are using AI like a search engine. "
    "You are asking it questions and copying the answer into a document. "
    "But that is not where the leverage is. "
    "The thing is, I built a 2 million dollar business with zero full time staff. "
    "I did it by hiring AI staff instead of humans. "
    "Every one of my departments is an agent with a job description and a boundary. "
    "My marketing department writes in my voice because I taught it my voice. "
    "Actually the hardest part was never the technology. "
    "It was writing down what I already knew. "
    "So if your AI keeps giving you generic output, the problem is not the model. "
    "The problem is that you never told it who you are. "
    "Start there and everything downstream changes. "
    "Anyway that is kind of all I wanted to say about that I guess. "
    "Let me know if that was helpful or whatever."
)

"""The word-level transcript: the spine everything downstream hangs off.

Captions, beat marks and clip selection all need to know exactly when each word
was said. Sentence-level timing cannot drive any of them, so word timings are
treated as required, not optional.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

_SENTENCE_END = re.compile(r"[.!?]+[\"')\]]*$")
_WORD_CHARS = re.compile(r"[^\w'-]+", re.UNICODE)


@dataclass(frozen=True)
class Word:
    text: str
    start: float
    end: float
    probability: float = 1.0

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)

    @property
    def clean(self) -> str:
        """The word with punctuation stripped, lowercased, for matching."""
        return _WORD_CHARS.sub("", self.text).lower()

    @property
    def ends_sentence(self) -> bool:
        return bool(_SENTENCE_END.search(self.text.strip()))


@dataclass
class Transcript:
    words: list[Word] = field(default_factory=list)
    language: str = "en"
    source: str = ""

    def __len__(self) -> int:
        return len(self.words)

    @property
    def duration(self) -> float:
        return self.words[-1].end if self.words else 0.0

    @property
    def text(self) -> str:
        return " ".join(w.text.strip() for w in self.words).strip()

    def words_between(self, start: float, end: float) -> list[Word]:
        """Words whose midpoint falls inside the window.

        Midpoint rather than full containment, so a word straddling a boundary
        lands on one side only and is never both dropped and duplicated.
        """
        return [w for w in self.words if start <= (w.start + w.end) / 2 < end]

    def text_between(self, start: float, end: float) -> str:
        return " ".join(w.text.strip() for w in self.words_between(start, end)).strip()

    def gap_after(self, index: int) -> float:
        """Silence between word `index` and the next one."""
        if index < 0 or index >= len(self.words) - 1:
            return 0.0
        return max(0.0, self.words[index + 1].start - self.words[index].end)

    def sentence_starts(self) -> list[int]:
        """Indices of words that begin a sentence."""
        if not self.words:
            return []
        starts = [0]
        for i, word in enumerate(self.words[:-1]):
            if word.ends_sentence:
                starts.append(i + 1)
        return starts

    def sentence_ends(self) -> list[int]:
        """Indices of words that end a sentence (last word always counts)."""
        ends = [i for i, w in enumerate(self.words) if w.ends_sentence]
        last = len(self.words) - 1
        if last >= 0 and (not ends or ends[-1] != last):
            ends.append(last)
        return ends

    # ---- serialisation ---------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "language": self.language,
            "source": self.source,
            "words": [
                {
                    "text": w.text,
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "probability": round(w.probability, 4),
                }
                for w in self.words
            ],
        }

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: str | Path) -> "Transcript":
        """Read our own format, or a Whisper JSON with word timestamps.

        Accepts openai-whisper and whisper-ctranslate2 output directly, so a
        transcript produced by any of them can be dropped straight in.
        """
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data, source=str(path))

    @classmethod
    def from_dict(cls, data: dict, *, source: str = "") -> "Transcript":
        language = data.get("language", "en")
        raw_words: list[dict] = []
        if isinstance(data.get("words"), list):
            raw_words = data["words"]
        elif isinstance(data.get("segments"), list):
            for segment in data["segments"]:
                raw_words.extend(segment.get("words") or [])
        else:
            raise ValueError(
                "transcript JSON has neither 'words' nor 'segments'. "
                "Re-run Whisper with word timestamps enabled."
            )

        words: list[Word] = []
        for item in raw_words:
            text = item.get("text", item.get("word", ""))
            if text is None:
                continue
            text = str(text).strip()
            if not text:
                continue
            start, end = item.get("start"), item.get("end")
            if start is None or end is None:
                continue
            start, end = float(start), float(end)
            if end < start:
                end = start
            words.append(Word(
                text=text,
                start=start,
                end=end,
                probability=float(
                    item.get("probability", item.get("confidence", 1.0)) or 1.0
                ),
            ))
        if not words:
            raise ValueError(
                "no word-level timings found. Whisper must be run with "
                "--word_timestamps True; sentence timing cannot drive captions."
            )
        words.sort(key=lambda w: (w.start, w.end))
        return cls(words=words, language=language, source=source or data.get("source", ""))

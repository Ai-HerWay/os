"""Word-level transcription with faster-whisper.

This is the only stage that needs a model download. It is also the only stage
that is genuinely slow, so its output is cached in the work folder and reused
on every later run.
"""

from __future__ import annotations

from pathlib import Path

from .ffmpeg import extract_audio
from .transcript import Transcript, Word


class TranscriberMissing(RuntimeError):
    pass


def transcribe(
    source: str | Path,
    *,
    model: str = "medium.en",
    language: str | None = "en",
    compute_type: str = "int8",
    device: str = "auto",
    work_dir: str | Path | None = None,
    vad_filter: bool = True,
) -> Transcript:
    """Transcribe `source` with word-level timings.

    `medium.en` is the default because it is the smallest model that reliably
    gets word boundaries right on conversational speech. `small.en` is roughly
    three times faster and noticeably worse at exactly the thing this pipeline
    depends on, so drop to it only for a rough pass.
    """
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise TranscriberMissing(
            "faster-whisper is not installed. Run `pip install faster-whisper`. "
            "Alternatively, transcribe elsewhere with word timestamps enabled "
            "and pass the JSON in with --transcript."
        ) from exc

    source = Path(source)
    audio_path = source
    if work_dir is not None:
        audio_path = extract_audio(source, Path(work_dir) / "audio.wav")

    whisper = WhisperModel(model, device=device, compute_type=compute_type)
    segments, info = whisper.transcribe(
        str(audio_path),
        language=language,
        word_timestamps=True,
        vad_filter=vad_filter,
    )

    words: list[Word] = []
    for segment in segments:
        for word in (segment.words or []):
            text = (word.word or "").strip()
            if not text:
                continue
            words.append(Word(
                text=text,
                start=float(word.start),
                end=float(word.end),
                probability=float(getattr(word, "probability", 1.0) or 1.0),
            ))

    if not words:
        raise ValueError(
            f"{source.name} produced no words. Check the file actually has "
            "speech on its audio track, and that it is not silent or music-only."
        )

    return Transcript(
        words=words,
        language=getattr(info, "language", language or "en"),
        source=str(source),
    )


def load_or_transcribe(
    source: str | Path,
    cache_path: str | Path,
    *,
    transcript_path: str | Path | None = None,
    force: bool = False,
    **kwargs,
) -> Transcript:
    """Return a cached transcript where one exists, otherwise make one.

    Order of preference: an explicitly supplied transcript, then the cache,
    then a fresh run of the model.
    """
    if transcript_path:
        return Transcript.load(transcript_path)
    cache_path = Path(cache_path)
    if cache_path.exists() and not force:
        return Transcript.load(cache_path)
    transcript = transcribe(source, work_dir=cache_path.parent, **kwargs)
    transcript.save(cache_path)
    return transcript

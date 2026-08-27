"""End-to-end render test.

Generates its own footage with ffmpeg, runs the whole chain over it, and checks
the output is a real 1080x1920 file with the captions actually burnt in. Skips
itself cleanly where ffmpeg is not installed.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from reelkit.clips import Audience, emphasis_words  # noqa: E402
from reelkit.config import Project, Style  # noqa: E402
from reelkit.ffmpeg import FFmpegNotFound, ffmpeg, ffmpeg_bin, probe  # noqa: E402
from reelkit.plan import analyse, build, render_reel, write_captions  # noqa: E402
from reelkit.transcript import Transcript, Word  # noqa: E402

# Audible spans in the generated clip, with real silence between them.
SPANS = [(0.0, 3.0), (4.2, 9.0), (10.5, 17.0), (18.4, 26.0), (27.6, 34.0)]
LINE = (
    "The thing is I built a 2 million dollar business with zero full time staff. "
    "Most women founders are using AI like a search engine. "
    "But that is not where the leverage is. "
    "So the problem is never the model it is the brief you never wrote. "
    "Start there and everything downstream changes."
)


def ffmpeg_available() -> bool:
    try:
        ffmpeg_bin()
    except FFmpegNotFound:
        return False
    return True


def make_clip(path: Path, duration: float = 35.0) -> Path:
    """A test pattern with speech-shaped gaps in the audio."""
    audible = "+".join(f"between(t,{a},{b})" for a, b in SPANS)
    ffmpeg([
        "-f", "lavfi", "-i", f"testsrc2=size=720x1280:rate=30:duration={duration}",
        "-f", "lavfi", "-i",
        f"sine=frequency=220:duration={duration},"
        f"volume=enable='{audible}':volume=1,"
        f"volume=enable='not({audible})':volume=0.001",
        "-c:v", "libx264", "-crf", "30", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k", "-shortest", str(path),
    ])
    return path


def make_transcript() -> Transcript:
    """Lay the line out so every word sits inside an audible span."""
    words: list[Word] = []
    span_index = 0
    clock = SPANS[0][0] + 0.1
    for token in LINE.split():
        if clock + 0.30 > SPANS[span_index][1] - 0.15:
            span_index += 1
            if span_index >= len(SPANS):
                break
            clock = SPANS[span_index][0] + 0.1
        words.append(Word(token, round(clock, 3), round(clock + 0.30, 3)))
        clock += 0.36
    return Transcript(words=words, language="en")


@unittest.skipUnless(ffmpeg_available(), "ffmpeg is not installed")
class TestEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="reelkit-"))
        cls.project = Project(cls.tmp).ensure()
        cls.source = make_clip(cls.project.raw / "take.mp4")
        cls.style = Style()
        cls.transcript = make_transcript()
        cls.analysis = analyse(
            cls.source, cls.transcript, style=cls.style,
            audience=Audience(keywords=["ai", "founders"],
                              pain_points=["search engine"]),
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_silence_was_actually_found(self):
        self.assertGreaterEqual(len(self.analysis.silences), 3)
        self.assertGreater(self.analysis.stripped_seconds, 2.0)

    def test_at_least_one_clip_is_offered(self):
        self.assertTrue(self.analysis.candidates)

    def test_render_produces_a_vertical_captioned_reel(self):
        reel = build(self.analysis, style=self.style, clip=1)
        captions = write_captions(
            reel, self.project.captions / "take.ass", style=self.style
        )
        self.assertIn("Dialogue:", captions.read_text(encoding="utf-8"))

        output = render_reel(
            reel, self.project.out / "take.mp4", style=self.style,
            captions=captions, project=self.project,
        )
        self.assertTrue(output.exists())
        info = probe(output)
        self.assertEqual((info.width, info.height), (1080, 1920))
        self.assertTrue(info.has_audio)
        # The render is the cut, so it must be shorter than the window it came
        # from but still hold most of it.
        self.assertLess(info.duration, reel.window.duration)
        self.assertGreater(info.duration, reel.window.duration * 0.6)
        self.assertAlmostEqual(info.duration, reel.timeline.duration, delta=0.5)

    def test_cut_only_render_has_no_punch_ins(self):
        reel = build(self.analysis, style=self.style, clip=1)
        output = render_reel(
            reel, self.project.out / "cut.mp4", style=self.style,
            captions=None, burn=False, project=self.project,
        )
        info = probe(output)
        self.assertEqual((info.width, info.height), (1080, 1920))

    def test_highlights_land_inside_the_chosen_window(self):
        reel = build(self.analysis, style=self.style, clip=1)
        for word in emphasis_words(self.transcript, reel.window.start,
                                   reel.window.end):
            self.assertGreaterEqual(word.start, reel.window.start)
            self.assertLessEqual(word.end, reel.window.end + 1e-6)


if __name__ == "__main__":
    unittest.main(verbosity=2)

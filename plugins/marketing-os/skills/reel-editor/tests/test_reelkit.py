"""Tests for the parts that decide things.

The pure logic runs without ffmpeg or a Whisper model, so this suite is
runnable anywhere. The render tests skip themselves when ffmpeg is absent.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import SAMPLE_TAKE, build_transcript  # noqa: E402
from reelkit.beats import detect_beats, thin_beats  # noqa: E402
from reelkit.captions import (  # noqa: E402
    build_events, format_time, escape_text, render_ass,
)
from reelkit.clips import (  # noqa: E402
    Audience, emphasis_words, find_candidates, score_hook, sentences,
)
from reelkit.config import Style, hex_to_ass, slugify  # noqa: E402
from reelkit.lexicon import contains_phrase, is_number, PIVOT_PHRASES  # noqa: E402
from reelkit.render import build_filtergraph, RenderPlan, escape_filter_path  # noqa: E402
from reelkit.silence import (  # noqa: E402
    Segment, keep_segments, parse_silence_log, restrict_to, total_kept,
)
from reelkit.timeline import Timeline, build_shots  # noqa: E402
from reelkit.transcript import Transcript, Word  # noqa: E402


class TestColour(unittest.TestCase):
    def test_matches_the_design_system_worked_examples(self):
        # These three are stated in the design handover, byte order and all.
        self.assertEqual(hex_to_ass("#F2EBDD"), "&H00DDEBF2")
        self.assertEqual(hex_to_ass("#35241F"), "&H001F2435")
        self.assertEqual(hex_to_ass("#C4D6DA"), "&H00DAD6C4")

    def test_is_bgr_not_rgb(self):
        self.assertEqual(hex_to_ass("#FF0000"), "&H000000FF")
        self.assertEqual(hex_to_ass("#0000FF"), "&H00FF0000")

    def test_alpha(self):
        self.assertEqual(hex_to_ass("#FFFFFF", alpha=255), "&HFFFFFFFF")

    def test_rejects_nonsense(self):
        for bad in ("#GGG", "F1EAE", "", "#F1EAE1F"):
            with self.assertRaises(ValueError):
                hex_to_ass(bad)

    def test_slugify(self):
        self.assertEqual(slugify("Reel 03 - Final CUT"), "reel-03-final-cut")
        self.assertEqual(slugify("///"), "clip")


class TestSilence(unittest.TestCase):
    LOG = """
    [silencedetect @ 0x1] silence_start: 3.02
    [silencedetect @ 0x1] silence_end: 4.20 | silence_duration: 1.18
    [silencedetect @ 0x1] silence_start: 9.01
    [silencedetect @ 0x1] silence_end: 10.52 | silence_duration: 1.51
    """

    def test_parses_pairs(self):
        found = parse_silence_log(self.LOG)
        self.assertEqual(len(found), 2)
        self.assertAlmostEqual(found[0].start, 3.02)
        self.assertAlmostEqual(found[1].end, 10.52)

    def test_closes_a_trailing_silence_at_the_duration(self):
        log = self.LOG + "\n[silencedetect @ 0x1] silence_start: 30.0\n"
        found = parse_silence_log(log, duration=40.0)
        self.assertEqual(len(found), 3)
        self.assertAlmostEqual(found[-1].end, 40.0)

    def test_trailing_silence_dropped_without_a_duration(self):
        log = self.LOG + "\n[silencedetect @ 0x1] silence_start: 30.0\n"
        self.assertEqual(len(parse_silence_log(log)), 2)

    def test_keep_segments_invert_and_pad(self):
        keeps = keep_segments([Segment(3.0, 5.0)], 10.0, pad=0.12)
        self.assertEqual(len(keeps), 2)
        # The keep runs 0.12s *into* the silence, leaving room tone.
        self.assertAlmostEqual(keeps[0].end, 3.12)
        self.assertAlmostEqual(keeps[1].start, 4.88)

    def test_a_silence_shorter_than_two_pads_is_not_cut_at_all(self):
        keeps = keep_segments([Segment(3.0, 3.15)], 10.0, pad=0.12)
        self.assertEqual(len(keeps), 1)
        self.assertAlmostEqual(total_kept(keeps), 10.0)

    def test_no_silence_keeps_everything(self):
        keeps = keep_segments([], 12.0)
        self.assertEqual(len(keeps), 1)
        self.assertAlmostEqual(total_kept(keeps), 12.0)

    def test_restrict_to_window(self):
        keeps = [Segment(0, 5), Segment(6, 12)]
        got = restrict_to(keeps, Segment(4, 8))
        self.assertEqual([(g.start, g.end) for g in got], [(4, 5), (6, 8)])


class TestTranscript(unittest.TestCase):
    def test_reads_openai_whisper_segment_format(self):
        data = {"language": "en", "segments": [
            {"words": [{"word": " Hello", "start": 0.0, "end": 0.4},
                       {"word": " world.", "start": 0.4, "end": 0.9}]},
        ]}
        t = Transcript.from_dict(data)
        self.assertEqual(len(t), 2)
        self.assertEqual(t.words[0].text, "Hello")
        self.assertTrue(t.words[1].ends_sentence)

    def test_refuses_a_transcript_without_word_timings(self):
        with self.assertRaises(ValueError) as ctx:
            Transcript.from_dict({"segments": [{"text": "no words here"}]})
        self.assertIn("word-level", str(ctx.exception))

    def test_sentence_boundaries(self):
        t = build_transcript("One two. Three four five! Six?")
        self.assertEqual(len(sentences(t)), 3)

    def test_words_between_uses_midpoints(self):
        t = build_transcript("alpha beta gamma delta")
        picked = t.words_between(0.0, t.words[2].start)
        self.assertEqual([w.text for w in picked], ["alpha", "beta"])

    def test_clean_strips_punctuation(self):
        self.assertEqual(Word("Don't,", 0, 1).clean, "don't")


class TestLexicon(unittest.TestCase):
    def test_numbers(self):
        for value in ("40", "$2M", "80%", "3x", "million", "2,000"):
            self.assertTrue(is_number(value), value)
        for value in ("business", "the", ""):
            self.assertFalse(is_number(value), value)

    def test_phrases_match_across_punctuation(self):
        self.assertTrue(
            contains_phrase("The thing is, I built it.", PIVOT_PHRASES)
        )


class TestHookScoring(unittest.TestCase):
    def test_a_warm_up_opener_scores_near_zero(self):
        weak, _ = score_hook("So um I just wanted to jump on here today.")
        strong, _ = score_hook("Most founders are using AI like a search engine.")
        self.assertLess(weak, 0.2)
        self.assertGreater(strong, weak)

    def test_numbers_and_pivots_are_rewarded(self):
        plain, _ = score_hook("I built a business with no staff.")
        loaded, _ = score_hook("The thing is, I built a 2 million dollar business.")
        self.assertGreater(loaded, plain)

    def test_every_score_is_bounded(self):
        for line in ("", "?", SAMPLE_TAKE, "you you you 1 2 3 why how what"):
            value, _ = score_hook(line)
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)


class TestCandidates(unittest.TestCase):
    def setUp(self):
        self.transcript = build_transcript(SAMPLE_TAKE)

    def test_candidates_respect_the_length_band(self):
        found = find_candidates(self.transcript, min_seconds=20, max_seconds=45)
        self.assertTrue(found)
        for candidate in found:
            self.assertGreaterEqual(candidate.duration, 20)
            self.assertLessEqual(candidate.duration, 45)

    def test_candidates_do_not_overlap_heavily(self):
        found = find_candidates(self.transcript, limit=4)
        for a, b in zip(found, found[1:]):
            inner = min(a.end, b.end) - max(a.start, b.start)
            if inner > 0:
                self.assertLess(inner / min(a.duration, b.duration), 0.51)

    def test_none_open_on_the_warm_up_waffle(self):
        found = find_candidates(self.transcript, limit=5)
        for candidate in found:
            self.assertFalse(candidate.hook_line.lower().startswith("so um"))

    def test_resonance_is_neutral_and_says_so_when_unconfigured(self):
        found = find_candidates(self.transcript, limit=1)[0]
        self.assertEqual(found.scores["resonance"], 0.5)
        self.assertIn("neutral", " ".join(found.notes["resonance"]))

    def test_a_configured_audience_moves_the_score(self):
        audience = Audience(
            keywords=["ai", "founders", "voice"],
            pain_points=["generic output"],
        )
        with_profile = find_candidates(self.transcript, audience=audience, limit=1)[0]
        self.assertNotEqual(with_profile.scores["resonance"], 0.5)

    def test_short_take_yields_nothing_rather_than_guessing(self):
        short = build_transcript("Too short to post. Really.")
        self.assertEqual(find_candidates(short, min_seconds=20), [])

    def test_highlights_avoid_stopwords_and_are_spaced(self):
        picks = emphasis_words(self.transcript, 0, self.transcript.duration, limit=5)
        self.assertLessEqual(len(picks), 5)
        for word in picks:
            self.assertNotIn(word.clean, {"you", "the", "what", "one"})
        for a, b in zip(picks, picks[1:]):
            self.assertGreater(b.start - a.start, 1.0)


class TestBeats(unittest.TestCase):
    def setUp(self):
        self.transcript = build_transcript(SAMPLE_TAKE)
        self.beats = detect_beats(self.transcript)

    def test_finds_numbers_and_pivots(self):
        kinds = {b.kind for b in self.beats}
        self.assertIn("number", kinds)
        self.assertIn("pivot", kinds)

    def test_thinning_respects_the_minimum_gap(self):
        thinned = thin_beats(self.beats, start=0, end=self.transcript.duration,
                             min_gap=2.0, max_gap=3.0)
        cuts = [b for b in thinned if b.action == "cut"]
        for a, b in zip(cuts, cuts[1:]):
            self.assertGreaterEqual(round(b.time - a.time, 3), 2.0)

    def test_frame_changes_land_near_one_every_two_to_three_seconds(self):
        span = self.transcript.duration
        thinned = thin_beats(self.beats, start=0, end=span)
        self.assertGreater(len(thinned), span / 4.0)
        self.assertLess(len(thinned), span / 1.5)

    def test_a_long_hold_is_marked_for_a_card_not_an_invented_cut(self):
        from reelkit.beats import Beat
        thinned = thin_beats([Beat(2.0, "number", "2", 0.9)],
                             start=0, end=30, max_gap=3.0)
        cards = [b for b in thinned if b.action == "card"]
        self.assertTrue(cards)
        # The real beat is kept, and nothing was invented as a cut.
        self.assertEqual(len([b for b in thinned if b.action == "cut"]), 1)

    def test_a_stretch_with_no_beats_at_all_is_all_cards(self):
        thinned = thin_beats([], start=0, end=20, max_gap=3.0)
        self.assertTrue(thinned)
        self.assertTrue(all(b.action == "card" for b in thinned))

    def test_a_marginal_overshoot_does_not_get_a_card(self):
        transcript = build_transcript("One two three. Four five six.")
        beats = thin_beats(detect_beats(transcript), start=0, end=3.4, max_gap=3.0)
        self.assertFalse(any(b.action == "card" for b in beats))


class TestTimeline(unittest.TestCase):
    def setUp(self):
        self.timeline = Timeline([Segment(0, 3), Segment(5, 9)])

    def test_duration_excludes_what_was_cut(self):
        self.assertAlmostEqual(self.timeline.duration, 7.0)

    def test_maps_across_the_join(self):
        self.assertAlmostEqual(self.timeline.map_time(1.0), 1.0)
        self.assertAlmostEqual(self.timeline.map_time(6.0), 4.0)

    def test_a_cut_out_moment_has_no_output_time(self):
        self.assertIsNone(self.timeline.map_time(4.0))

    def test_clamping_snaps_to_the_nearest_surviving_frame(self):
        self.assertAlmostEqual(self.timeline.map_time_clamped(4.0), 3.0)
        self.assertAlmostEqual(self.timeline.map_time_clamped(99.0), 7.0)
        self.assertAlmostEqual(self.timeline.map_time_clamped(-1.0), 0.0)

    def test_empty_timeline_is_falsy(self):
        self.assertFalse(Timeline([]))


class TestShots(unittest.TestCase):
    def setUp(self):
        self.transcript = build_transcript(SAMPLE_TAKE)
        self.beats = thin_beats(detect_beats(self.transcript), start=0,
                                end=self.transcript.duration)
        self.keeps = [Segment(0, 30), Segment(31, 60)]
        self.shots = build_shots(self.keeps, self.beats)

    def test_shots_tile_the_kept_footage_exactly(self):
        self.assertAlmostEqual(
            sum(s.duration for s in self.shots), total_kept(self.keeps), places=5
        )

    def test_output_times_are_contiguous(self):
        for a, b in zip(self.shots, self.shots[1:]):
            self.assertAlmostEqual(a.out_end, b.out_start, places=5)

    def test_zoom_never_repeats_back_to_back(self):
        for a, b in zip(self.shots, self.shots[1:]):
            self.assertNotEqual(a.zoom, b.zoom)

    def test_shots_never_cross_a_silence_cut(self):
        for shot in self.shots:
            self.assertTrue(any(
                k.start - 1e-6 <= shot.source_start and shot.source_end <= k.end + 1e-6
                for k in self.keeps
            ))

    def test_a_beat_just_after_a_silence_cut_does_not_make_a_flash_frame(self):
        from reelkit.beats import Beat
        # The beat lands 0.22s into the second segment. It cannot merge
        # backwards - that would cross the silence cut - so the boundary has
        # to go instead.
        segments = [Segment(0, 3.14), Segment(4.08, 9.13)]
        beats = [Beat(2.26, "number", "2", 0.9), Beat(4.30, "number", "2", 0.9)]
        shots = build_shots(segments, beats, min_shot=0.6)
        for shot in shots:
            self.assertGreaterEqual(shot.duration, 0.6)

    def test_a_short_tail_merges_into_the_shot_before_it(self):
        from reelkit.beats import Beat
        segments = [Segment(0, 5.0)]
        shots = build_shots(segments, [Beat(4.8, "pivot", "but", 0.7)],
                            min_shot=0.6)
        self.assertEqual(len(shots), 1)
        self.assertAlmostEqual(shots[0].duration, 5.0)

    def test_a_frame_too_short_to_read_is_absorbed(self):
        shots = build_shots([Segment(0, 10)], self.beats, min_shot=0.6)
        for shot in shots:
            self.assertGreaterEqual(shot.duration, 0.6 - 1e-6)


class TestCaptions(unittest.TestCase):
    def setUp(self):
        self.style = Style()
        self.transcript = build_transcript("One two three. Four five six.")
        self.timeline = Timeline([Segment(0, self.transcript.duration + 1)])

    def test_time_format(self):
        self.assertEqual(format_time(0), "0:00:00.00")
        self.assertEqual(format_time(61.5), "0:01:01.50")
        self.assertEqual(format_time(3661.239), "1:01:01.24")
        self.assertEqual(format_time(-5), "0:00:00.00")

    def test_escaping(self):
        self.assertEqual(escape_text("a{b}c"), "a\\{b\\}c")
        self.assertEqual(escape_text("line\nbreak"), "line break")

    def test_one_word_per_event(self):
        events = build_events(self.transcript, self.timeline, style=self.style)
        self.assertEqual(len(events), len(self.transcript))
        for event in events:
            self.assertNotIn(" ", event.text.strip())

    def test_events_never_overlap(self):
        events = build_events(self.transcript, self.timeline, style=self.style)
        for a, b in zip(events, events[1:]):
            self.assertLessEqual(a.end, b.start + 1e-9)

    def test_words_inside_a_sentence_butt_together(self):
        events = build_events(self.transcript, self.timeline, style=self.style)
        self.assertAlmostEqual(events[0].end, events[1].start, places=6)

    def test_a_real_pause_stays_empty(self):
        events = build_events(self.transcript, self.timeline, style=self.style)
        gaps = [b.start - a.end for a, b in zip(events, events[1:])]
        self.assertTrue(any(gap > 0.3 for gap in gaps))

    def test_uppercase_applied(self):
        events = build_events(self.transcript, self.timeline, style=self.style)
        self.assertEqual(events[0].text, "ONE")

    def test_highlight_style_is_applied_to_the_chosen_words(self):
        chosen = [self.transcript.words[1]]
        ass = render_ass(self.transcript, self.timeline, style=self.style,
                         highlight=chosen)
        self.assertIn(",Highlight,", ass)
        self.assertEqual(ass.count(",Highlight,"), 1)

    def test_header_carries_the_brand_colours_in_ass_byte_order(self):
        ass = render_ass(self.transcript, self.timeline, style=self.style)
        self.assertIn(hex_to_ass(self.style.caption.text_hex), ass)
        self.assertIn(hex_to_ass(self.style.caption.highlight_block_hex), ass)
        self.assertIn("PlayResY: 1920", ass)

    def test_highlight_uses_an_opaque_box(self):
        ass = render_ass(self.transcript, self.timeline, style=self.style)
        highlight_line = next(
            l for l in ass.splitlines() if l.startswith("Style: Highlight")
        )
        # BorderStyle 3 is what turns the outline colour into a solid block.
        self.assertEqual(highlight_line.split(",")[15], "3")


class TestRenderGraph(unittest.TestCase):
    def setUp(self):
        self.style = Style()
        self.shots = build_shots(
            [Segment(0, 12)],
            thin_beats(detect_beats(build_transcript(SAMPLE_TAKE)), start=0, end=12),
        )

    def _plan(self, **kwargs):
        return RenderPlan(source=Path("in.mp4"), shots=self.shots,
                          output=Path("out.mp4"), style=self.style, **kwargs)

    def test_graph_splits_once_per_shot(self):
        graph = build_filtergraph(self._plan())
        self.assertIn(f"split={len(self.shots)}", graph)
        self.assertIn(f"concat=n={len(self.shots)}:v=1:a=1", graph)

    def test_output_labels_always_exist(self):
        graph = build_filtergraph(self._plan())
        self.assertIn("[outv]", graph)
        self.assertIn("[outa]", graph)

    def test_silent_source_produces_no_audio_branch(self):
        graph = build_filtergraph(self._plan(has_audio=False))
        self.assertNotIn("[outa]", graph)
        self.assertIn("concat=n=%d:v=1:a=0" % len(self.shots), graph)

    def test_crop_dimensions_are_even(self):
        graph = build_filtergraph(self._plan())
        import re
        for width, height in re.findall(r"crop=(\d+):(\d+):", graph):
            self.assertEqual(int(width) % 2, 0)
            self.assertEqual(int(height) % 2, 0)

    def test_captions_are_burnt_after_the_concat(self):
        graph = build_filtergraph(self._plan(captions=Path("/tmp/c.ass")))
        self.assertLess(graph.index("concat="), graph.index("ass=filename="))

    def test_empty_shot_list_is_an_error_not_an_empty_render(self):
        plan = RenderPlan(source=Path("in.mp4"), shots=[],
                          output=Path("out.mp4"), style=self.style)
        with self.assertRaises(ValueError):
            build_filtergraph(plan)

    def test_filter_paths_escape_colons(self):
        self.assertEqual(escape_filter_path("C:/a.ass"), "C\\:/a.ass")


if __name__ == "__main__":
    unittest.main(verbosity=2)

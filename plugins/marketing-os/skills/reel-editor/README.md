# reelkit

The pipeline behind the `reel-editor` skill. Drop an unedited talking-head file in `raw/`, and
this takes it to a finished 1080x1920 MP4: transcribed, silence-stripped, punched in on the
beats, captioned in brand.

It runs on your machine, not in a chat window, for three reasons. Raw files are 200MB to 2GB and
uploading them twice per attempt is a twenty minute round trip. Transcription has to happen on
the file, and locally that is a couple of minutes. And editing is iterative: you will want to
nudge a punch-in and re-render, and that loop belongs on your machine.

## Install

```bash
brew install ffmpeg          # macOS. Windows: winget install ffmpeg
pip install faster-whisper
```

Fonts: install Montserrat system-wide, not just in Canva. libass reads system fonts, so a font
that only exists inside a design tool will silently fall back to something else.

No install step for reelkit itself. From this directory:

```bash
python3 -m reelkit --help
```

To run it from anywhere, put this on your `PYTHONPATH` or add an alias:

```bash
alias reelkit='PYTHONPATH=/path/to/reel-editor python3 -m reelkit'
```

If ffmpeg is somewhere unusual, set `REELKIT_FFMPEG` (and `REELKIT_FFPROBE`) to the binaries.
ffprobe is optional: where it is missing, the media header is read from ffmpeg directly.

## Folder shape

```
reels/
  raw/         untouched footage straight off the phone
  work/        transcript, analysis, edit plan, shot list, intermediate renders
  overlays/    the PNG kit, reusable across every reel
  sfx/         sound files, reusable
  out/         finished 1080x1920 MP4s
  captions/    generated .ass files, one per reel
```

Point at it with `--project reels`, or run from inside it.

## Use it

```bash
reelkit --project reels ingest raw/take-04.mp4     # transcribe + find the silence
reelkit --project reels plan take-04               # rank the clips, write the edit plan
```

`plan` writes `work/take-04/EDIT-PLAN.md` and stops. Read it, pick a clip, then:

```bash
reelkit --project reels cut take-04 --clip 1       # silence strip only. Listen to this first.
reelkit --project reels captions take-04 --clip 1  # the .ass, for CapCut
reelkit --project reels render take-04 --clip 1    # the finished reel
```

Do not skip `cut`. A bad silence strip is invisible until you hear it, and everything else gets
built on top of it.

Other things you will want:

```bash
--window 112 144        # cut an explicit source window instead of a ranked clip
--audience aud.json     # make the resonance score mean something
--transcript w.json     # use a Whisper JSON you already have
--silence-db -26        # noisy room: air conditioning, traffic
--no-burn               # keep the captions as a separate .ass
--overlay overlays/frame.png --click-sfx sfx/click.wav
```

## How a clip gets chosen

Every sentence-aligned window in the 20 to 45 second band is scored out of 100 on six things
that can be read straight off the transcript:

| Dimension | Weight | What it measures |
|---|---|---|
| hook | 30 | How the opening line is built: direct address, a concrete number, a question, a spoken pivot, and how fast it gets to the point |
| resonance | 20 | How much of the audience profile's language and stated pain points the clip touches |
| cleanliness | 15 | Filler density and dead air |
| payoff | 15 | Whether the closing line resolves rather than trails off |
| pace | 10 | Words per second against a 2.3 to 3.6 band |
| shape | 10 | Length inside the band, and a clean sentence-boundary start |

Overlapping windows are suppressed, so the five results are genuinely different clips rather than
five shifts of the same one.

Two things this deliberately does not do. It does not predict performance: it describes
properties of the transcript, and the edit plan shows every reason so you can disagree with it.
And without an audience profile it scores resonance neutral and says so, rather than quietly
passing a craft-only ranking off as audience fit.

### The audience profile

Copy `styles/audience.example.json` and fill it from `memory/business-context.md`:

```json
{
  "name": "women founders building with AI",
  "keywords": ["ai", "founders", "voice", "agent", "leverage"],
  "pain_points": ["generic output", "search engine", "never told it"],
  "avoid": ["hustle", "crush it"]
}
```

`keywords` is the language your audience uses. `pain_points` are problems they have said out
loud. `avoid` is language that is off-brand, and it costs a clip points.

### Cold opens

Where a line later in the clip would hook harder than the one it opens on, the plan surfaces it
with its score. Moving it to the front is a reorder of words she already said, never a rewrite.
It is offered, not applied.

## The style preset

`styles/aiherway.json` holds the caption styling, the punch-in schedule and the cut settings.
The colours are AI Her Way's: Linen `#F1EAE1` type, Charcoal `#252620` shadow, and Charcoal on a
Misty Sage `#C0CACE` block for the 3 to 5 highlighted words.

One thing worth knowing if you edit it by hand: ASS colours are `&HAABBGGRR`. Alpha first, then
**blue, green, red**, not RGB. `#F1EAE1` becomes `&H00E1EAF1`. This catches everyone. The
conversion lives in `reelkit/config.py` so nothing else has to get it right.

## Tuning the cut

| Symptom | Fix |
|---|---|
| Nothing was stripped | The room was noisy. `--silence-db -26` |
| Too much was stripped, it sounds choppy | `--silence-db -38`, or raise `silence_min_duration` |
| The cuts sound clipped | Raise `pad` above 0.12s. This is room tone, not threshold |
| Captions are hard to read on a phone | The size or the shadow is wrong, not the font. Raise `shadow`, or `outline` above 0 |
| Captions are the wrong font | libass reads system fonts. Install Montserrat properly, or `--font "Your Font"` |
| The frame changes feel frantic | Raise `beat_min_gap` |
| It sits too long on one frame | Lower `beat_max_gap`, or add the graphic cards the shot list asks for |

## CapCut

CapCut has no API and no MCP connector, so nothing drives it programmatically from outside. The
desktop version stores each project as a folder of JSON on disk, which in principle means a draft
could be generated: that is an afternoon's experiment, not a plan, and the schema changes between
versions.

The reliable path is what this pipeline already produces: a pre-cut video, an `.ass` caption file
and the overlay PNGs. Import those three and the manual work left is arranging overlays and
dropping sound.

## Tests

```bash
python3 tests/test_reelkit.py              # pure logic, no ffmpeg needed
python3 tests/test_render_integration.py   # generates footage and renders it
```

The integration suite makes its own test clip with real silence in it, runs the whole chain, and
checks the output is a 1080x1920 file with captions burnt in. It skips itself where ffmpeg is
absent.

## What it will not do

It will not add a word to a caption that is not in the transcript, join two unrelated sentences
into a claim that was never made, put a statistic or testimonial on screen that was not spoken,
or publish anything. Renders stop in `out/`.

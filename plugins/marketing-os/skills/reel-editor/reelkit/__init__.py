"""reelkit - the AI Her Way reel editing pipeline.

Drop an unedited talking-head file in `raw/`, and this package takes it through
transcription, silence stripping, clip selection, caption generation and render
to a finished 1080x1920 MP4.

Nothing here publishes anything. Every stage writes to disk and stops.
"""

__version__ = "1.0.0"

__all__ = ["__version__"]

"""Project layout, brand style, and the hex-to-ASS colour conversion.

The one thing worth knowing here: ASS colours are `&HAABBGGRR` - alpha first,
then *blue, green, red*, not RGB. Getting that backwards is the single most
common way a brand palette comes out looking wrong, so it is converted in one
place and nowhere else.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

# --------------------------------------------------------------------------
# Colour
# --------------------------------------------------------------------------

_HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6})$")


def hex_to_ass(hex_colour: str, alpha: int = 0) -> str:
    """Convert `#RRGGBB` to an ASS `&HAABBGGRR` string.

    `alpha` is ASS alpha, where 0 is fully opaque and 255 fully transparent.
    """
    match = _HEX_RE.match(hex_colour.strip())
    if not match:
        raise ValueError(
            f"{hex_colour!r} is not a 6-digit hex colour like '#F1EAE1'"
        )
    if not 0 <= alpha <= 255:
        raise ValueError(f"ASS alpha must be 0-255, got {alpha}")
    digits = match.group(1).upper()
    red, green, blue = digits[0:2], digits[2:4], digits[4:6]
    return f"&H{alpha:02X}{blue}{green}{red}"


# --------------------------------------------------------------------------
# Style
# --------------------------------------------------------------------------


@dataclass
class CaptionStyle:
    """Everything that decides how a burnt-in word looks."""

    font: str = "Montserrat SemiBold"
    fallback_font: str = "DejaVu Sans"
    size: int = 78
    text_hex: str = "#F1EAE1"          # Linen
    outline_hex: str = "#252620"       # Charcoal
    shadow_hex: str = "#252620"        # Charcoal
    highlight_text_hex: str = "#252620"   # Charcoal type ...
    highlight_block_hex: str = "#C0CACE"  # ... on a Misty Sage block
    outline: float = 0.0
    shadow: float = 6.0
    margin_v: int = 300
    margin_h: int = 60
    bold: bool = False
    uppercase: bool = True


@dataclass
class RenderStyle:
    """Frame, motion and export settings."""

    width: int = 1080
    height: int = 1920
    fps: int = 30
    crf: int = 20
    preset: str = "medium"
    audio_bitrate: str = "192k"
    # Punch-in: alternate between these zoom levels on each beat.
    zoom_levels: list[float] = field(default_factory=lambda: [1.0, 1.12])
    # 0.5 centres the face; lower lifts the crop so the eyes sit on the
    # upper third, which is where they belong in a vertical frame.
    eyeline: float = 0.35
    # Never let more than this many punch-ins run back to back before the
    # editor is told to break the rhythm with a graphic card instead.
    max_consecutive_punches: int = 2


@dataclass
class EditStyle:
    """How the cut itself is made."""

    silence_db: int = -32
    silence_min_duration: float = 0.35
    # Room tone left on each side of a cut so it does not sound clipped.
    pad: float = 0.12
    # Target one frame change every N seconds.
    beat_min_gap: float = 2.0
    beat_max_gap: float = 3.0
    # A candidate reel should land inside this length band.
    clip_min_seconds: float = 20.0
    clip_max_seconds: float = 45.0


@dataclass
class Style:
    name: str = "aiherway"
    caption: CaptionStyle = field(default_factory=CaptionStyle)
    render: RenderStyle = field(default_factory=RenderStyle)
    edit: EditStyle = field(default_factory=EditStyle)

    # ---- serialisation ---------------------------------------------------

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Style":
        """Load a style preset. With no path, the built-in default is used."""
        if path is None:
            return cls()
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "Style":
        return cls(
            name=data.get("name", "custom"),
            caption=CaptionStyle(**data.get("caption", {})),
            render=RenderStyle(**data.get("render", {})),
            edit=EditStyle(**data.get("edit", {})),
        )

    def to_dict(self) -> dict:
        return asdict(self)

    # ---- derived ---------------------------------------------------------

    @property
    def ass_text(self) -> str:
        return hex_to_ass(self.caption.text_hex)

    @property
    def ass_outline(self) -> str:
        return hex_to_ass(self.caption.outline_hex)

    @property
    def ass_shadow(self) -> str:
        return hex_to_ass(self.caption.shadow_hex)

    @property
    def ass_highlight_text(self) -> str:
        return hex_to_ass(self.caption.highlight_text_hex)

    @property
    def ass_highlight_block(self) -> str:
        return hex_to_ass(self.caption.highlight_block_hex)


# --------------------------------------------------------------------------
# Project layout
# --------------------------------------------------------------------------


@dataclass
class Project:
    """The folder shape the pipeline works in.

    reels/
      raw/        untouched footage straight off the phone
      work/       intermediate artefacts, one folder per source clip
      overlays/   the PNG kit, reusable across every reel
      sfx/        sound files, reusable
      out/        finished 1080x1920 MP4s
      captions/   generated .ass files
    """

    root: Path

    def __post_init__(self) -> None:
        self.root = Path(self.root).expanduser().resolve()

    @property
    def raw(self) -> Path:
        return self.root / "raw"

    @property
    def work(self) -> Path:
        return self.root / "work"

    @property
    def overlays(self) -> Path:
        return self.root / "overlays"

    @property
    def sfx(self) -> Path:
        return self.root / "sfx"

    @property
    def out(self) -> Path:
        return self.root / "out"

    @property
    def captions(self) -> Path:
        return self.root / "captions"

    def workdir(self, slug: str) -> Path:
        return self.work / slug

    def ensure(self) -> "Project":
        for folder in (
            self.raw, self.work, self.overlays,
            self.sfx, self.out, self.captions,
        ):
            folder.mkdir(parents=True, exist_ok=True)
        return self


def slugify(value: str) -> str:
    """Filename-safe slug, used to name the work folder for a source clip."""
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", str(value)).strip("-").lower()
    return cleaned or "clip"

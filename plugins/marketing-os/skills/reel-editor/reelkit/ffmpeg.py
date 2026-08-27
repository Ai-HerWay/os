"""Finding, running and interrogating ffmpeg.

Every shell-out in the pipeline goes through here so there is exactly one place
that knows where the binary lives and one place that raises a readable error
when a render fails.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


class FFmpegNotFound(RuntimeError):
    pass


class FFmpegFailed(RuntimeError):
    """Raised with the tail of ffmpeg's stderr, which is where the reason is."""

    def __init__(self, args: list[str], returncode: int, stderr: str):
        self.args_run = args
        self.returncode = returncode
        self.stderr = stderr
        tail = "\n".join(stderr.strip().splitlines()[-15:])
        super().__init__(
            f"ffmpeg exited {returncode}.\n"
            f"command: {' '.join(args[:6])} ... ({len(args)} args)\n"
            f"stderr tail:\n{tail}"
        )


def _from_imageio(name: str) -> str | None:
    """imageio-ffmpeg ships a static build; use it if it is installed."""
    if name != "ffmpeg":
        return None
    try:
        import imageio_ffmpeg  # type: ignore
    except ImportError:
        return None
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def _locate(name: str, env_var: str) -> str:
    override = os.environ.get(env_var)
    if override:
        if not Path(override).exists():
            raise FFmpegNotFound(f"{env_var}={override} does not exist")
        return override
    found = shutil.which(name)
    if found:
        return found
    bundled = _from_imageio(name)
    if bundled:
        return bundled
    raise FFmpegNotFound(
        f"{name} is not on PATH. Install it (macOS: `brew install ffmpeg`), "
        f"or point {env_var} at the binary."
    )


def ffmpeg_bin() -> str:
    return _locate("ffmpeg", "REELKIT_FFMPEG")


def ffprobe_bin() -> str:
    """The ffprobe path, or None-ish via FFmpegNotFound.

    Some static ffmpeg builds ship without ffprobe. `probe()` falls back to
    parsing `ffmpeg -i` output in that case, so this raising is not fatal.
    """
    return _locate("ffprobe", "REELKIT_FFPROBE")


def has_ffprobe() -> bool:
    try:
        ffprobe_bin()
    except FFmpegNotFound:
        return False
    return True


def run(args: list[str], *, capture: bool = True) -> subprocess.CompletedProcess:
    """Run an ffmpeg-family command, raising FFmpegFailed on a non-zero exit."""
    proc = subprocess.run(
        args,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        text=True,
    )
    if proc.returncode != 0:
        raise FFmpegFailed(args, proc.returncode, proc.stderr or "")
    return proc


def ffmpeg(args: list[str], *, overwrite: bool = True) -> subprocess.CompletedProcess:
    cmd = [ffmpeg_bin(), "-hide_banner", "-nostdin"]
    cmd.append("-y" if overwrite else "-n")
    cmd += args
    return run(cmd)


@dataclass
class MediaInfo:
    path: Path
    duration: float
    width: int
    height: int
    fps: float
    has_audio: bool
    sample_rate: int | None = None

    @property
    def is_vertical(self) -> bool:
        return self.height >= self.width


def _parse_fps(rate: str | None) -> float:
    if not rate:
        return 0.0
    if "/" in rate:
        num, _, den = rate.partition("/")
        try:
            den_f = float(den)
            return float(num) / den_f if den_f else 0.0
        except ValueError:
            return 0.0
    try:
        return float(rate)
    except ValueError:
        return 0.0


_DURATION_RE = re.compile(r"Duration:\s*(\d+):(\d\d):(\d\d(?:\.\d+)?)")
_VIDEO_RE = re.compile(r"Stream #\d+:\d+.*: Video:.*?(\d{2,5})x(\d{2,5})")
_VIDEO_FPS_RE = re.compile(r"(\d+(?:\.\d+)?)\s+fps")
_AUDIO_RE = re.compile(r"Stream #\d+:\d+.*: Audio:")
_AUDIO_HZ_RE = re.compile(r"Audio:.*?(\d+)\s*Hz")


def _probe_via_ffmpeg(path: Path) -> MediaInfo:
    """Fallback probe for builds that ship ffmpeg without ffprobe.

    `ffmpeg -i` with no output exits non-zero by design, so the header is read
    off stderr rather than through run().
    """
    proc = subprocess.run(
        [ffmpeg_bin(), "-hide_banner", "-nostdin", "-i", str(path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    text = proc.stderr or ""
    duration_match = _DURATION_RE.search(text)
    if not duration_match:
        raise FFmpegFailed([ffmpeg_bin(), "-i", str(path)], proc.returncode, text)
    hours, minutes, seconds = duration_match.groups()
    duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)

    video_match = _VIDEO_RE.search(text)
    if not video_match:
        raise ValueError(f"{path} has no video stream")
    width, height = int(video_match.group(1)), int(video_match.group(2))

    video_line = text[video_match.start():text.find("\n", video_match.start())]
    fps_match = _VIDEO_FPS_RE.search(video_line)
    fps = float(fps_match.group(1)) if fps_match else 0.0

    audio_match = _AUDIO_RE.search(text)
    hz_match = _AUDIO_HZ_RE.search(text) if audio_match else None
    return MediaInfo(
        path=path,
        duration=duration,
        width=width,
        height=height,
        fps=fps,
        has_audio=audio_match is not None,
        sample_rate=int(hz_match.group(1)) if hz_match else None,
    )


def probe(path: str | Path) -> MediaInfo:
    """Read duration, dimensions, frame rate and audio presence."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"no such media file: {path}")
    if not has_ffprobe():
        return _probe_via_ffmpeg(path)
    proc = run([
        ffprobe_bin(), "-v", "error",
        "-print_format", "json",
        "-show_format", "-show_streams",
        str(path),
    ])
    data = json.loads(proc.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if video is None:
        raise ValueError(f"{path} has no video stream")
    duration = float(data.get("format", {}).get("duration") or 0.0)
    if not duration:
        duration = float(video.get("duration") or 0.0)
    return MediaInfo(
        path=path,
        duration=duration,
        width=int(video.get("width") or 0),
        height=int(video.get("height") or 0),
        fps=_parse_fps(video.get("avg_frame_rate") or video.get("r_frame_rate")),
        has_audio=audio is not None,
        sample_rate=int(audio["sample_rate"]) if audio and audio.get("sample_rate") else None,
    )


def extract_audio(source: str | Path, dest: str | Path, *, sample_rate: int = 16000) -> Path:
    """Pull a mono 16 kHz WAV, which is what the transcriber wants."""
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg([
        "-i", str(source),
        "-vn", "-ac", "1", "-ar", str(sample_rate),
        "-c:a", "pcm_s16le",
        str(dest),
    ])
    return dest

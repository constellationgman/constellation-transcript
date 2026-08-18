"""
Caption retrieval and parsing for Constellation Transcript.

Temporary subtitle files are created only inside the local cache folder
and are deleted after being read.
"""

from dataclasses import dataclass
from html import unescape
from pathlib import Path
import re
import shutil
import tempfile

import yt_dlp

from config import CACHE_DIRECTORY


@dataclass(frozen=True)
class TranscriptResult:
    """A retrieved caption transcript."""

    text: str
    language: str


class TranscriptError(RuntimeError):
    """Raised when captions cannot be retrieved or processed."""


_TIMESTAMP_LINE = re.compile(
    r"^\d{2}:\d{2}:\d{2}[.,]\d{3}\s+-->\s+"
    r"\d{2}:\d{2}:\d{2}[.,]\d{3}"
)

_TAG = re.compile(r"<[^>]+>")
_WHITESPACE = re.compile(r"\s+")


def _clean_vtt(vtt_text: str) -> str:
    """Convert WebVTT caption content into readable plain text."""
    cleaned_lines: list[str] = []
    previous_line = ""

    for raw_line in vtt_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line == "WEBVTT":
            continue

        if line.startswith(("Kind:", "Language:", "NOTE")):
            continue

        if _TIMESTAMP_LINE.match(line):
            continue

        if line.isdigit():
            continue

        line = _TAG.sub("", line)
        line = unescape(line)
        line = _WHITESPACE.sub(" ", line).strip()

        if not line or line == previous_line:
            continue

        cleaned_lines.append(line)
        previous_line = line

    transcript = "\n".join(cleaned_lines).strip()

    if not transcript:
        raise TranscriptError("The downloaded caption file contained no text.")

    return transcript


def get_transcript(url: str) -> TranscriptResult:
    """
    Retrieve English captions without downloading video or audio.

    Manually supplied English subtitles are preferred. Automatic English
    captions are used when manual captions are unavailable.
    """
    CACHE_DIRECTORY.mkdir(parents=True, exist_ok=True)

    temporary_directory = Path(
        tempfile.mkdtemp(prefix="job-", dir=CACHE_DIRECTORY)
    )

    output_template = str(temporary_directory / "%(id)s.%(ext)s")

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en", "en-US", "en-GB"],
        "subtitlesformat": "vtt",
        "outtmpl": output_template,
    }

    try:
        with yt_dlp.YoutubeDL(options) as client:
            client.extract_info(url, download=True)

        caption_files = sorted(temporary_directory.glob("*.vtt"))

        if not caption_files:
            raise TranscriptError(
                "No downloadable English captions were found."
            )

        caption_path = caption_files[0]
        caption_text = caption_path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        language = caption_path.stem.split(".")[-1]

        return TranscriptResult(
            text=_clean_vtt(caption_text),
            language=language,
        )

    except yt_dlp.utils.DownloadError as error:
        raise TranscriptError(
            "YouTube captions could not be retrieved."
        ) from error

    except OSError as error:
        raise TranscriptError(
            "The temporary caption file could not be processed."
        ) from error

    finally:
        shutil.rmtree(temporary_directory, ignore_errors=True)

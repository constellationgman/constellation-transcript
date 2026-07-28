"""
Public YouTube metadata retrieval.

This module does not download video, audio, captions, or thumbnails.
"""

from dataclasses import dataclass
from typing import Any

import yt_dlp


@dataclass(frozen=True)
class VideoInfo:
    """Public metadata returned for one YouTube video."""

    title: str
    channel: str
    duration_seconds: int | None
    captions_available: bool


class YouTubeClientError(RuntimeError):
    """Raised when public YouTube metadata cannot be retrieved."""


def _captions_are_available(info: dict[str, Any]) -> bool:
    """Return True when manual or automatic captions are listed."""
    subtitles = info.get("subtitles") or {}
    automatic_captions = info.get("automatic_captions") or {}

    return bool(subtitles or automatic_captions)


def get_video_info(url: str) -> VideoInfo:
    """
    Retrieve public metadata without downloading media.

    No files are created by this function.
    """
    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(options) as client:
            info = client.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as error:
        raise YouTubeClientError(
            "YouTube metadata could not be retrieved."
        ) from error

    if not isinstance(info, dict):
        raise YouTubeClientError(
            "YouTube returned an unexpected metadata response."
        )

    title = str(info.get("title") or "Unknown title")
    channel = str(
        info.get("channel")
        or info.get("uploader")
        or "Unknown channel"
    )

    raw_duration = info.get("duration")
    duration = raw_duration if isinstance(raw_duration, int) else None

    return VideoInfo(
        title=title,
        channel=channel,
        duration_seconds=duration,
        captions_available=_captions_are_available(info),
    )


"""
Central configuration for Constellation Transcript.
"""

from pathlib import Path

PROGRAM_NAME = "Constellation Transcript"
VERSION = "0.9.0"

OUTPUT_DIRECTORY = (
    Path.home()
    / "storage"
    / "shared"
    / "Documents"
    / "YouTubeText"
)

CACHE_DIRECTORY = (
    Path.home()
    / "constellation-transcript"
    / "cache"
)

ALLOWED_YOUTUBE_HOSTS = frozenset(
    {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
        "youtu.be",
    }
)

MAX_URL_LENGTH = 2048

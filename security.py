"""
Input validation for Constellation Transcript.
"""

from urllib.parse import urlparse

from config import ALLOWED_YOUTUBE_HOSTS, MAX_URL_LENGTH


def is_valid_youtube_url(value: str) -> bool:
    """Return True only for approved HTTPS YouTube URLs."""
    cleaned = value.strip()

    if not cleaned or len(cleaned) > MAX_URL_LENGTH:
        return False

    try:
        parsed = urlparse(cleaned)
    except ValueError:
        return False

    if parsed.scheme != "https":
        return False

    if parsed.hostname not in ALLOWED_YOUTUBE_HOSTS:
        return False

    if parsed.username is not None or parsed.password is not None:
        return False

    if parsed.port not in (None, 443):
        return False

    if parsed.hostname == "youtu.be":
        return bool(parsed.path.strip("/"))

    return parsed.path in {
        "/watch",
        "/shorts",
        "/live",
    } or parsed.path.startswith(
        (
            "/watch/",
            "/shorts/",
            "/live/",
        )
    )


def validate_youtube_url(value: str) -> str:
    """Return a cleaned approved URL or raise ValueError."""
    cleaned = value.strip()

    if not is_valid_youtube_url(cleaned):
        raise ValueError(
            "That is not an accepted YouTube HTTPS link."
        )

    return cleaned


def get_valid_youtube_url() -> str:
    """Prompt until the user enters an approved YouTube URL."""
    while True:
        value = input("Paste YouTube URL: ")

        try:
            return validate_youtube_url(value)
        except ValueError as error:
            print(f"{error} Please try again.")

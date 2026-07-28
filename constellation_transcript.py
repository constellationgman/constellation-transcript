#!/usr/bin/env python3

"""
Constellation Transcript

A local-first utility for converting available YouTube captions into
verified text files.

Security boundaries:
- No listening network ports
- No remote administration
- No telemetry
- No hidden functionality
- No media download when captions are available
"""

import sys

from config import PROGRAM_NAME, VERSION
from export import ExportError, export_transcript
from security import get_valid_youtube_url, validate_youtube_url
from transcript import TranscriptError, get_transcript
from youtube_client import YouTubeClientError, get_video_info


def format_duration(seconds: int | None) -> str:
    """Convert seconds into a readable duration."""
    if seconds is None:
        return "Unknown"

    hours, remainder = divmod(seconds, 3600)
    minutes, remaining_seconds = divmod(remainder, 60)

    if hours:
        return f"{hours}:{minutes:02d}:{remaining_seconds:02d}"

    return f"{minutes}:{remaining_seconds:02d}"


def get_input_url(arguments: list[str]) -> str:
    """
    Read a YouTube URL from the command line or prompt interactively.

    Android Share integration supplies exactly one command-line value.
    """
    if len(arguments) == 1:
        return get_valid_youtube_url()

    if len(arguments) > 2:
        raise ValueError("Only one YouTube URL may be supplied.")

    return validate_youtube_url(arguments[1])


def main() -> int:
    print(PROGRAM_NAME)
    print(f"Version {VERSION}")
    print()

    try:
        url = get_input_url(sys.argv)
    except ValueError as error:
        print(f"Error: {error}")
        return 2

    print()
    print("Retrieving public video information...")

    try:
        info = get_video_info(url)
    except YouTubeClientError as error:
        print()
        print(f"Error: {error}")
        return 1

    print()
    print("=" * 48)
    print("Video Information")
    print("=" * 48)
    print(f"Title: {info.title}")
    print(f"Channel: {info.channel}")
    print(f"Duration: {format_duration(info.duration_seconds)}")
    print(
        "Captions available: "
        + ("Yes" if info.captions_available else "No")
    )

    if not info.captions_available:
        print()
        print("No captions are available.")
        print("No file was created.")
        return 1

    print()
    print("Retrieving English captions...")

    try:
        transcript = get_transcript(url)
    except TranscriptError as error:
        print()
        print(f"Error: {error}")
        print("No file was created.")
        return 1

    print()
    print(f"Caption language: {transcript.language}")
    print("Temporary caption files deleted.")
    print()
    print("Exporting and verifying transcript...")

    try:
        output_path = export_transcript(
            title=info.title,
            transcript_text=transcript.text,
        )
    except ExportError as error:
        print()
        print(f"Error: {error}")
        return 1

    print()
    print("=" * 48)
    print("Export successful")
    print("=" * 48)
    print(f"Saved to: {output_path}")
    print("Verification: Passed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

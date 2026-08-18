"""
Controlled filesystem operations for Constellation Transcript.

This is the only module permitted to create final transcript files.
"""

import os
import re
import tempfile
from pathlib import Path

from config import OUTPUT_DIRECTORY


class FilesystemError(RuntimeError):
    """Raised when a controlled filesystem operation fails."""


_INVALID_FILENAME_CHARACTERS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_REPEATED_WHITESPACE = re.compile(r"\s+")
_REPEATED_DASHES = re.compile(r"-{2,}")

_MAX_FILENAME_LENGTH = 120


def sanitize_filename(title: str) -> str:
    """
    Convert a video title into a safe, portable filename.

    Directory separators, control characters, and characters that commonly
    fail on other operating systems are removed.
    """
    cleaned = _INVALID_FILENAME_CHARACTERS.sub(" - ", title)
    cleaned = _REPEATED_WHITESPACE.sub(" ", cleaned)
    cleaned = _REPEATED_DASHES.sub("-", cleaned)
    cleaned = cleaned.strip(" .-_")

    if not cleaned:
        cleaned = "YouTube Transcript"

    return cleaned[:_MAX_FILENAME_LENGTH].rstrip(" .-_")


def ensure_output_directory() -> Path:
    """Create and return the approved transcript output directory."""
    try:
        OUTPUT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )
    except OSError as error:
        raise FilesystemError(
            "The transcript output directory could not be created."
        ) from error

    if not OUTPUT_DIRECTORY.is_dir():
        raise FilesystemError(
            "The configured transcript output path is not a directory."
        )

    return OUTPUT_DIRECTORY


def _available_output_path(filename_stem: str) -> Path:
    """
    Return an unused output path.

    Existing transcript files are never overwritten.
    """
    output_directory = ensure_output_directory()

    first_candidate = output_directory / f"{filename_stem}.txt"

    if not first_candidate.exists():
        return first_candidate

    number = 2

    while number <= 9999:
        candidate = output_directory / f"{filename_stem} ({number}).txt"

        if not candidate.exists():
            return candidate

        number += 1

    raise FilesystemError(
        "A unique transcript filename could not be created."
    )


def write_text_atomically(title: str, text: str) -> Path:
    """
    Write a complete UTF-8 text file using a temporary file.

    The final transcript appears only after the entire write succeeds.
    Existing files are not deliberately overwritten.
    """
    if not isinstance(text, str) or not text.strip():
        raise FilesystemError(
            "An empty transcript cannot be exported."
        )

    output_directory = ensure_output_directory()
    safe_title = sanitize_filename(title)
    destination = _available_output_path(safe_title)

    temporary_path: Path | None = None

    try:
        file_descriptor, temporary_name = tempfile.mkstemp(
            prefix=".yt2text-",
            suffix=".tmp",
            dir=output_directory,
        )

        temporary_path = Path(temporary_name)

        with os.fdopen(
            file_descriptor,
            mode="w",
            encoding="utf-8",
            newline="\n",
        ) as temporary_file:
            temporary_file.write(text.strip())
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        if destination.exists():
            destination = _available_output_path(safe_title)

        os.replace(temporary_path, destination)
        temporary_path = None

        return destination

    except OSError as error:
        raise FilesystemError(
            "The transcript could not be written safely."
        ) from error

    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass


def verify_text_file(path: Path, expected_text: str) -> bool:
    """
    Verify that an exported file contains the expected transcript.

    The comparison ignores only the final newline added during export.
    """
    try:
        actual_text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise FilesystemError(
            "The exported transcript could not be verified."
        ) from error

    return actual_text.rstrip("\n") == expected_text.strip()

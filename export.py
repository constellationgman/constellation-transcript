"""
Transcript export interface for YouTube to Text.
"""

from pathlib import Path

from filesystem import (
    FilesystemError,
    verify_text_file,
    write_text_atomically,
)


class ExportError(RuntimeError):
    """Raised when a transcript cannot be exported and verified."""


def export_transcript(title: str, transcript_text: str) -> Path:
    """
    Export and verify one transcript.

    The file is considered successfully exported only after its contents
    have been read back and compared with the original transcript.
    """
    try:
        output_path = write_text_atomically(
            title=title,
            text=transcript_text,
        )

        if not verify_text_file(output_path, transcript_text):
            try:
                output_path.unlink(missing_ok=True)
            except OSError:
                pass

            raise ExportError(
                "Transcript verification failed. "
                "The unverified file was removed."
            )

        return output_path

    except FilesystemError as error:
        raise ExportError(str(error)) from error

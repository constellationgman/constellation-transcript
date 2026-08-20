import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import filesystem
from export import ExportError, export_transcript


class ExportTests(unittest.TestCase):
    def test_successful_export_returns_verified_file(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(
                filesystem,
                "OUTPUT_DIRECTORY",
                Path(directory),
            ):
                path = export_transcript(
                    title="Test Video",
                    transcript_text="Verified transcript.",
                )

                self.assertTrue(path.exists())
                self.assertEqual(
                    path.read_text(encoding="utf-8"),
                    "Verified transcript.\n",
                )

    def test_verification_failure_removes_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output_directory = Path(directory)

            with patch.object(
                filesystem,
                "OUTPUT_DIRECTORY",
                output_directory,
            ), patch(
                "export.verify_text_file",
                return_value=False,
            ):
                with self.assertRaises(ExportError):
                    export_transcript(
                        title="Test Video",
                        transcript_text="Unverified transcript.",
                    )

                self.assertEqual(
                    list(output_directory.iterdir()),
                    [],
                )


if __name__ == "__main__":
    unittest.main()

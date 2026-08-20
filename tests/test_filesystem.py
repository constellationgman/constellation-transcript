import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import filesystem
from filesystem import sanitize_filename, verify_text_file, write_text_atomically


class FilenameTests(unittest.TestCase):
    def test_keeps_normal_title(self):
        self.assertEqual(
            sanitize_filename("My YouTube Video"),
            "My YouTube Video",
        )

    def test_removes_path_characters(self):
        result = sanitize_filename('Bad/Title\\Name')

        self.assertNotIn("/", result)
        self.assertNotIn("\\", result)

    def test_removes_unsafe_filename_characters(self):
        result = sanitize_filename('<Bad>:"Title"|?*')

        for character in '<>:"|?*':
            self.assertNotIn(character, result)

    def test_empty_title_gets_safe_default(self):
        self.assertEqual(
            sanitize_filename("   "),
            "YouTube Transcript",
        )

    def test_limits_filename_length(self):
        result = sanitize_filename("A" * 500)

        self.assertLessEqual(len(result), 120)


class FilesystemWriteTests(unittest.TestCase):
    def test_writes_and_verifies_transcript(self):
        with tempfile.TemporaryDirectory() as directory:
            output_directory = Path(directory)

            with patch.object(
                filesystem,
                "OUTPUT_DIRECTORY",
                output_directory,
            ):
                path = write_text_atomically(
                    "Test Video",
                    "Hello world.",
                )

                self.assertTrue(path.exists())
                self.assertTrue(
                    verify_text_file(
                        path,
                        "Hello world.",
                    )
                )

    def test_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output_directory = Path(directory)

            with patch.object(
                filesystem,
                "OUTPUT_DIRECTORY",
                output_directory,
            ):
                first = write_text_atomically(
                    "Test Video",
                    "First transcript.",
                )

                second = write_text_atomically(
                    "Test Video",
                    "Second transcript.",
                )

                self.assertNotEqual(first, second)
                self.assertEqual(
                    first.read_text(encoding="utf-8"),
                    "First transcript.\n",
                )
                self.assertEqual(
                    second.read_text(encoding="utf-8"),
                    "Second transcript.\n",
                )

    def test_rejects_empty_transcript(self):
        with tempfile.TemporaryDirectory() as directory:
            output_directory = Path(directory)

            with patch.object(
                filesystem,
                "OUTPUT_DIRECTORY",
                output_directory,
            ):
                with self.assertRaises(
                    filesystem.FilesystemError
                ):
                    write_text_atomically(
                        "Test Video",
                        "   ",
                    )


if __name__ == "__main__":
    unittest.main()

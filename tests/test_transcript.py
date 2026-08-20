import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from yt_dlp.utils import DownloadError

import transcript
from transcript import (
    TranscriptError,
    _clean_vtt,
    get_transcript,
)


class TranscriptCleanupTests(unittest.TestCase):
    def test_cleans_basic_vtt(self):
        vtt = """WEBVTT

00:00:01.000 --> 00:00:03.000
Hello world.

00:00:03.000 --> 00:00:05.000
This is a transcript.
"""

        self.assertEqual(
            _clean_vtt(vtt),
            "Hello world.\nThis is a transcript.",
        )

    def test_removes_duplicate_consecutive_lines(self):
        vtt = """WEBVTT

Hello world.
Hello world.
Different line.
"""

        self.assertEqual(
            _clean_vtt(vtt),
            "Hello world.\nDifferent line.",
        )

    def test_removes_html_tags_and_decodes_entities(self):
        vtt = """WEBVTT

<c>Hello &amp; welcome.</c>
"""

        self.assertEqual(
            _clean_vtt(vtt),
            "Hello & welcome.",
        )

    def test_rejects_empty_caption_content(self):
        with self.assertRaises(TranscriptError):
            _clean_vtt("WEBVTT\n\n")

    def test_ignores_vtt_metadata(self):
        vtt = """WEBVTT
Kind: captions
Language: en

Hello world.
"""

        self.assertEqual(
            _clean_vtt(vtt),
            "Hello world.",
        )

    def test_normalizes_whitespace(self):
        vtt = """WEBVTT

Hello      world.
This    has     spaces.
"""

        self.assertEqual(
            _clean_vtt(vtt),
            "Hello world.\nThis has spaces.",
        )

    def test_keeps_nonconsecutive_duplicate_lines(self):
        vtt = """WEBVTT

First line.
Second line.
First line.
"""

        self.assertEqual(
            _clean_vtt(vtt),
            "First line.\nSecond line.\nFirst line.",
        )

    def test_removes_numeric_caption_sequence_lines(self):
        vtt = """WEBVTT

1
00:00:01.000 --> 00:00:02.000
First line.

2
00:00:02.000 --> 00:00:03.000
Second line.
"""

        self.assertEqual(
            _clean_vtt(vtt),
            "First line.\nSecond line.",
        )


class TranscriptRetrievalTests(unittest.TestCase):
    @patch("transcript.yt_dlp.YoutubeDL")
    def test_retrieves_caption_and_cleans_temp_directory(
        self,
        mock_youtube_dl,
    ):
        with tempfile.TemporaryDirectory() as directory:
            cache_directory = Path(directory)

            client = MagicMock()
            mock_youtube_dl.return_value.__enter__.return_value = client

            def create_caption_file(url, download):
                job_directories = list(
                    cache_directory.glob("job-*")
                )
                self.assertEqual(len(job_directories), 1)

                caption_path = (
                    job_directories[0]
                    / "test.en.vtt"
                )

                caption_path.write_text(
                    """WEBVTT

00:00:01.000 --> 00:00:02.000
Hello from captions.
""",
                    encoding="utf-8",
                )

                return {}

            client.extract_info.side_effect = create_caption_file

            with patch.object(
                transcript,
                "CACHE_DIRECTORY",
                cache_directory,
            ):
                result = get_transcript(
                    "https://www.youtube.com/watch?v=test"
                )

            self.assertEqual(
                result.text,
                "Hello from captions.",
            )
            self.assertEqual(result.language, "en")
            self.assertEqual(
                list(cache_directory.glob("job-*")),
                [],
            )

    @patch("transcript.yt_dlp.YoutubeDL")
    def test_cleans_temp_directory_after_ytdlp_failure(
        self,
        mock_youtube_dl,
    ):
        with tempfile.TemporaryDirectory() as directory:
            cache_directory = Path(directory)

            client = MagicMock()
            mock_youtube_dl.return_value.__enter__.return_value = client
            client.extract_info.side_effect = DownloadError(
                "Simulated caption failure"
            )

            with patch.object(
                transcript,
                "CACHE_DIRECTORY",
                cache_directory,
            ):
                with self.assertRaises(TranscriptError):
                    get_transcript(
                        "https://www.youtube.com/watch?v=test"
                    )

            self.assertEqual(
                list(cache_directory.glob("job-*")),
                [],
            )

    @patch("transcript.yt_dlp.YoutubeDL")
    def test_cleans_temp_directory_when_no_caption_file_exists(
        self,
        mock_youtube_dl,
    ):
        with tempfile.TemporaryDirectory() as directory:
            cache_directory = Path(directory)

            client = MagicMock()
            mock_youtube_dl.return_value.__enter__.return_value = client
            client.extract_info.return_value = {}

            with patch.object(
                transcript,
                "CACHE_DIRECTORY",
                cache_directory,
            ):
                with self.assertRaises(TranscriptError):
                    get_transcript(
                        "https://www.youtube.com/watch?v=test"
                    )

            self.assertEqual(
                list(cache_directory.glob("job-*")),
                [],
            )


if __name__ == "__main__":
    unittest.main()

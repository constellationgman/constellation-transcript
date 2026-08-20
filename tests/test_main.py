import unittest
from unittest.mock import patch

import constellation_transcript
from export import ExportError
from transcript import TranscriptError, TranscriptResult
from youtube_client import VideoInfo, YouTubeClientError


TEST_URL = "https://www.youtube.com/watch?v=test"


class MainTests(unittest.TestCase):
    @patch(
        "constellation_transcript.sys.argv",
        [
            "constellation_transcript.py",
            TEST_URL,
            "https://youtu.be/two",
        ],
    )
    def test_too_many_arguments_returns_exit_code_2(self):
        self.assertEqual(
            constellation_transcript.main(),
            2,
        )

    @patch("constellation_transcript.get_video_info")
    @patch(
        "constellation_transcript.sys.argv",
        ["constellation_transcript.py", TEST_URL],
    )
    def test_metadata_failure_returns_exit_code_1(
        self,
        mock_get_video_info,
    ):
        mock_get_video_info.side_effect = YouTubeClientError(
            "Simulated metadata failure."
        )

        self.assertEqual(
            constellation_transcript.main(),
            1,
        )

    @patch("constellation_transcript.get_video_info")
    @patch(
        "constellation_transcript.sys.argv",
        ["constellation_transcript.py", TEST_URL],
    )
    def test_no_captions_returns_exit_code_1(
        self,
        mock_get_video_info,
    ):
        mock_get_video_info.return_value = VideoInfo(
            title="Test Video",
            channel="Test Channel",
            duration_seconds=60,
            captions_available=False,
        )

        self.assertEqual(
            constellation_transcript.main(),
            1,
        )

    @patch("constellation_transcript.get_transcript")
    @patch("constellation_transcript.get_video_info")
    @patch(
        "constellation_transcript.sys.argv",
        ["constellation_transcript.py", TEST_URL],
    )
    def test_transcript_failure_returns_exit_code_1(
        self,
        mock_get_video_info,
        mock_get_transcript,
    ):
        mock_get_video_info.return_value = VideoInfo(
            title="Test Video",
            channel="Test Channel",
            duration_seconds=60,
            captions_available=True,
        )
        mock_get_transcript.side_effect = TranscriptError(
            "Simulated transcript failure."
        )

        self.assertEqual(
            constellation_transcript.main(),
            1,
        )

    @patch("constellation_transcript.export_transcript")
    @patch("constellation_transcript.get_transcript")
    @patch("constellation_transcript.get_video_info")
    @patch(
        "constellation_transcript.sys.argv",
        ["constellation_transcript.py", TEST_URL],
    )
    def test_export_failure_returns_exit_code_1(
        self,
        mock_get_video_info,
        mock_get_transcript,
        mock_export_transcript,
    ):
        mock_get_video_info.return_value = VideoInfo(
            title="Test Video",
            channel="Test Channel",
            duration_seconds=60,
            captions_available=True,
        )
        mock_get_transcript.return_value = TranscriptResult(
            text="Test transcript.",
            language="en",
        )
        mock_export_transcript.side_effect = ExportError(
            "Simulated export failure."
        )

        self.assertEqual(
            constellation_transcript.main(),
            1,
        )

    @patch("constellation_transcript.export_transcript")
    @patch("constellation_transcript.get_transcript")
    @patch("constellation_transcript.get_video_info")
    @patch(
        "constellation_transcript.sys.argv",
        ["constellation_transcript.py", TEST_URL],
    )
    def test_success_returns_exit_code_0(
        self,
        mock_get_video_info,
        mock_get_transcript,
        mock_export_transcript,
    ):
        mock_get_video_info.return_value = VideoInfo(
            title="Test Video",
            channel="Test Channel",
            duration_seconds=125,
            captions_available=True,
        )
        mock_get_transcript.return_value = TranscriptResult(
            text="Test transcript.",
            language="en",
        )
        mock_export_transcript.return_value = (
            "/tmp/Test Video.txt"
        )

        self.assertEqual(
            constellation_transcript.main(),
            0,
        )


if __name__ == "__main__":
    unittest.main()

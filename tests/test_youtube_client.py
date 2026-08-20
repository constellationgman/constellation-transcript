from unittest.mock import MagicMock, patch

import unittest

from youtube_client import (
    _captions_are_available,
    get_video_info,
)


class YouTubeClientTests(unittest.TestCase):
    def test_manual_captions_are_detected(self):
        info = {
            "subtitles": {
                "en": [{"ext": "vtt"}]
            }
        }

        self.assertTrue(
            _captions_are_available(info)
        )
    def test_automatic_captions_are_detected(self):
        info = {
            "automatic_captions": {
                "en": [{"ext": "vtt"}]
            }
        }

        self.assertTrue(
            _captions_are_available(info)
        )

    def test_no_captions_returns_false(self):
        self.assertFalse(
            _captions_are_available({})
        )
    @patch("youtube_client.yt_dlp.YoutubeDL")
    def test_get_video_info_parses_metadata(self, mock_youtube_dl):
        client = MagicMock()
        mock_youtube_dl.return_value.__enter__.return_value = client

        client.extract_info.return_value = {
            "title": "Test Video",
            "channel": "Test Channel",
            "duration": 125,
            "subtitles": {
                "en": [{"ext": "vtt"}]
            },
        }

        info = get_video_info(
            "https://www.youtube.com/watch?v=test"
        )

        self.assertEqual(info.title, "Test Video")
        self.assertEqual(info.channel, "Test Channel")
        self.assertEqual(info.duration_seconds, 125)
        self.assertTrue(info.captions_available)

if __name__ == "__main__":
    unittest.main()


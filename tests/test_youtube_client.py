import unittest

from youtube_client import _captions_are_available


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

if __name__ == "__main__":
    unittest.main()


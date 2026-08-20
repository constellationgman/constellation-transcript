import unittest

from transcript import TranscriptError, _clean_vtt


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


if __name__ == "__main__":
    unittest.main()


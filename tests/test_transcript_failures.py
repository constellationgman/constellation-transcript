import unittest
from unittest.mock import patch

from transcript import TranscriptError, get_transcript


class TranscriptFailureTests(unittest.TestCase):
    @patch(
        "transcript.Path.mkdir",
        side_effect=OSError("Simulated cache failure"),
    )
    def test_cache_directory_failure_becomes_transcript_error(
        self,
        mock_mkdir,
    ):
        with self.assertRaises(TranscriptError):
            get_transcript(
                "https://www.youtube.com/watch?v=test"
            )


if __name__ == "__main__":
    unittest.main()

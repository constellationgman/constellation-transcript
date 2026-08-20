import unittest

from config import MAX_URL_LENGTH
from security import is_valid_youtube_url


class SecurityTests(unittest.TestCase):
    def test_accepts_standard_youtube_watch_url(self):
        self.assertTrue(
            is_valid_youtube_url(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )
        )

    def test_accepts_youtu_be_url(self):
        self.assertTrue(
            is_valid_youtube_url(
                "https://youtu.be/dQw4w9WgXcQ"
            )
        )

    def test_accepts_mobile_youtube_url(self):
        self.assertTrue(
            is_valid_youtube_url(
                "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
            )
        )

    def test_accepts_music_youtube_url(self):
        self.assertTrue(
            is_valid_youtube_url(
                "https://music.youtube.com/watch?v=dQw4w9WgXcQ"
            )
        )

    def test_rejects_http(self):
        self.assertFalse(
            is_valid_youtube_url(
                "http://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )
        )

    def test_rejects_unapproved_domain(self):
        self.assertFalse(
            is_valid_youtube_url(
                "https://example.com/watch?v=dQw4w9WgXcQ"
            )
        )

    def test_rejects_deceptive_suffix_domain(self):
        self.assertFalse(
            is_valid_youtube_url(
                "https://youtube.com.evil.example/watch?v=dQw4w9WgXcQ"
            )
        )

    def test_rejects_youtube_in_query_string(self):
        self.assertFalse(
            is_valid_youtube_url(
                "https://evil.example/?url=https://youtube.com/watch?v=x"
            )
        )

    def test_rejects_embedded_username(self):
        self.assertFalse(
            is_valid_youtube_url(
                "https://user@youtube.com/watch?v=dQw4w9WgXcQ"
            )
        )

    def test_rejects_nonstandard_port(self):
        self.assertFalse(
            is_valid_youtube_url(
                "https://youtube.com:444/watch?v=dQw4w9WgXcQ"
            )
        )

    def test_rejects_empty_input(self):
        self.assertFalse(is_valid_youtube_url(""))

    def test_rejects_overlength_input(self):
        value = "https://youtu.be/" + ("a" * MAX_URL_LENGTH)
        self.assertFalse(is_valid_youtube_url(value))

    def test_rejects_file_scheme(self):
        self.assertFalse(
            is_valid_youtube_url("file:///etc/passwd")
        )

    def test_rejects_javascript_scheme(self):
        self.assertFalse(
            is_valid_youtube_url("javascript:alert(1)")
        )


if __name__ == "__main__":
    unittest.main()

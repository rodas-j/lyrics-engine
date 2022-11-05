"""
This is a test file for the App python file.
"""
import unittest
from app import generate_lyricle, generate_lyricles_from_playlist

BEST_SONGS_OF_ALL_TIME = "0gqrnk12Q8OExuCeKyBRCq"


class TestLyricsGeniusAPIClient(unittest.TestCase):
    def test_generate_lyricles(self):
        generate_lyricles_from_playlist(BEST_SONGS_OF_ALL_TIME, limit=2)


if __name__ == "__main__":
    unittest.main()

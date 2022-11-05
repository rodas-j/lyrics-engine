"""
This is a test file for the Spotify API python file.
"""
import unittest
from soundcloud_api_client import SongDoesntExistError
from absl.testing import parameterized
from spotify_api_client import SpotifyAPIClient

BEST_SONGS_OF_THE_21ST_CENTURY = "5FyBhvR8ioYHBaJMXAt7yS"
BEST_SONGS_OF_THE_20TH_CENTURY = "4OQaRbhuJJETp6Q0cmhiay"
TWENTY_FIRST_CENTURY = "3IBFMXSXSdaI1r6RG59Sus"
BEST_SONGS_OF_ALL_TIME = "0gqrnk12Q8OExuCeKyBRCq"


class TestSpotifyAPIClient(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.play_list = [
            BEST_SONGS_OF_ALL_TIME,
            BEST_SONGS_OF_THE_21ST_CENTURY,
            TWENTY_FIRST_CENTURY,
            BEST_SONGS_OF_THE_20TH_CENTURY,
        ]
        self.play_list_lengths = [508, 335, 739, 368]

    def test_get_playlist_tracks(self):
        for playlist in self.play_list:
            SpotifyAPIClient.get_playlist_tracks(playlist)

    def test_get_song_tuples_from_playlist(self):
        SpotifyAPIClient.get_song_tuples_from_playlist(BEST_SONGS_OF_ALL_TIME)

    def test_search(self):
        song_name = "Lazy Song"
        artist = "Bruno Mars"
        SpotifyAPIClient.search_track(song_name, artist)
        with self.assertRaises(SongDoesntExistError):
            song_name = "Stairway to Heaven - 1990 Remaster"
            artist = "BLed Zeppelin"
            SpotifyAPIClient.search_track(song_name, artist)

    def test_clean_tags(self):
        tracks = [
            ("Beautiful People", "Ed Sheeran"),
            ("Street Fighting Man", "The Rolling Stones"),
        ]
        for t in tracks:
            track = SpotifyAPIClient.search_track(*t)
            self.assertEqual(t[0], track["title"])


if __name__ == "__main__":
    unittest.main()

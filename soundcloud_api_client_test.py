"""
This is a test file for the SoundCloud API python file.
"""
from soundcloud_api_client import SongDoesntExistError, SoundCloudAPIClient
from spotify_api_client import SpotifyAPIClient
import unittest
from absl.testing import parameterized

BEST_SONGS_OF_ALL_TIME = "0gqrnk12Q8OExuCeKyBRCq"


class TestSoundCloudAPIClient(parameterized.TestCase):
    def setUp(self):
        self.url = "https://soundcloud.com/katyperry/firework"
        self.soundcloud_client = SoundCloudAPIClient()

    def test_get_song_from_url(self):
        response = self.soundcloud_client.get_song_from_url(self.url)
        self.assertNotEqual(response, {})
        self.assertIn("artwork_url", response)

    def test_get_artwork_url(self):
        artwork_url = self.soundcloud_client.get_artwork_url_from_url(self.url)
        self.assertRegexpMatches(
            artwork_url, "https://i1\.sndcdn\.com/artworks.*large\.jpg"
        )

    def test_search(self):
        query = "Adele Hello"
        self.soundcloud_client.search(query)

    def test_search_fails(self):
        query = "fslkjfw12"
        response = self.soundcloud_client.search(query)
        self.assertEqual(
            response, {**response, **{"collection": [], "total_results": 0}}
        )

    def test_get_song(self):
        query = "Adele Hello"
        response = self.soundcloud_client.get_first_song(query)
        self.assertEqual(
            response["artwork_url"],
            "https://i1.sndcdn.com/artworks-qWdKf5O63ifR-0-large.png",
        )

    def test_soundcloud_song_matches_spotipy(self):
        tracks = SpotifyAPIClient.get_playlist_tracks(BEST_SONGS_OF_ALL_TIME)
        for track in tracks[:15]:
            song_name = track["track"]["name"]
            artist_name = track["track"]["artists"][0]["name"]

            # query = " ".join((artist_name, song_name))
            try:
                response = self.soundcloud_client.get_verified_song(
                    artist_name, song_name
                )
            except SongDoesntExistError:
                continue
            soundcloud_artist = response["user"]["username"]

            self.assertIn(
                artist_name.lower(),
                soundcloud_artist.lower(),
                response["permalink_url"],
            )

    @parameterized.named_parameters(
        (
            "the_lazy_song",
            "https://soundcloud.com/brunomars/the─lazy─song",
            False,
        ),
        (
            "i_will_always_love_you",
            "https://soundcloud.com/whitneyhouston/i─will─always─love─you",
            False,
        ),
        (
            "bang_bang",
            "https://soundcloud.com/knaan-official/bang-bang",
            True,
        ),
    )
    def test_soundcloud_links(self, broken_link, works):
        self.assertEqual(
            self.soundcloud_client.is_valid_link(broken_link), works
        )


if __name__ == "__main__":
    unittest.main()

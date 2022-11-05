import unittest

from attr import asdict
from dataclasses import asdict

from lyricle import Lyricle


class TestLyricle(unittest.TestCase):
    # def test_generate_lyricle(self):
    #     song_data = Lyricle.generate_lyricle("Beautiful People", "Ed Sheeran")
    #     self.assertEqual(
    #         asdict(song_data),
    #         {
    #             "title": "Beautiful People",
    #             "artist": "Ed Sheeran",
    #             "lyrics": [
    #                 "We are, we are, we are",
    #                 "L.A. on a Saturday night in the summer",
    #                 "Sundown and they all come out",
    #                 "Lamborghinis and their rented Hummers",
    #                 "The party's on, so they're headin' downtown ('Round here)",
    #                 "Everybody's lookin' for a come up",
    #             ],
    #             "song_link": "https://soundcloud.com/edsheeran/beautiful-people-feat-khalid",
    #             "artwork_link": "https://i1.sndcdn.com/artworks-TtVL7y4jxVVz-0-large.jpg",
    #         },
    #     )

    def test_prince(self):
        song_data = Lyricle.generate_lyricle("Purple Rain", "Prince")

    def test_generate_lyricles_from_playlist(self):
        result = Lyricle.generate_lyricles_from_playlist(
            "5Rrf7mqN8uus2AaQQQNdc1", limit=5
        )
        self.assertEqual(5, len(result))

    def test_generate_lyricles_from_txt(self):
        result = Lyricle.generate_lyricles_from_txt("test_data/song.txt", 6)
        print(result)

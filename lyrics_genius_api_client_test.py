"""
This is a test file for the Lyrics Genius API python file.
"""
from lyrics_genius_api_client import BuggyLineException, LyricsGeniusAPIClient
import unittest


class TestLyricsGeniusAPIClient(unittest.TestCase):
    def setUp(self):
        self.genius_client = LyricsGeniusAPIClient()
        self.test_song = ("Hello", "Adele")
        # self.test_song = ("Late Night Talking", "Harry Styles")

    def test_limit(self):
        self.genius_client.limit = 10
        lyrics = self.genius_client.get_lyricle_list(*self.test_song)
        self.assertEqual(len(lyrics), 10)

    def test_default_limit(self):
        lyrics = self.genius_client.get_lyricle_list(*self.test_song)
        self.assertEqual(len(lyrics), 6)

    def test_get_lyricle_list_max_limit(self):
        self.genius_client.limit = LyricsGeniusAPIClient.MAX_LIMIT
        adele_song = ("Hello", "Adele")
        lyrics_lst = self.genius_client.get_lyricle_list(*adele_song)
        last_lyric = (
            "But it don't matter, it clearly doesn't tear you apart anymore"
        )

        self.assertEqual(lyrics_lst[len(lyrics_lst) - 1], last_lyric)

    def test_get_lyrics(self):
        self.genius_client.get_lyrics(*self.test_song)

    def test_get_lyrics_in_loop(self):
        for _ in range(5):
            self.genius_client.get_lyrics(*self.test_song)

    def test_get_lyricle_list(self):
        lyrics = self.genius_client.get_lyricle_list(*self.test_song)
        self.genius_client.assert_valid_lines(lyrics)

    def test_get_lyricle_lst_with_potentially_buggy(self):
        song_name = "Beautiful People"
        artist = "Ed Sheeran"
        print(self.genius_client.get_lyricle_list(song_name, artist))
        """
        "lyrics": [
                "Screenplay By Sam Hamm",
                "FIRST DRAFT",
                "NOTE: THE HARD COPY OF THIS SCRIPT CONTAINED SCENE NUMBERS.",
                "THEY HAVE BEEN REMOVED FOR THIS SOFT COPY.",
                "NOTE ALSO: THE HARD COPY OF THIS SCRIPT WAS IN THE NON-",
                'PREFORMAT FONT "BOOKMAN OLD". THIS HAS BEEN CHANGED TO',
            ]
        """
        song_name = "Ruby Tuesday"
        artist = "The Rolling Stones"
        # with self.assertRaises(Exception):
        self.genius_client.get_lyricle_list(song_name, artist)

    def test_assert_valid_lines_when_buggy(self):
        test_invalid = {
            "song": "Ed Sheeran ─ Beautiful People (feat. Khalid)",
            "lyrics": [
                "Daniel Caesar ─ LOVE AGAIN",
                "Chris Brown ─ Don't Check On Me (feat. Justin Bieber & Ink)",
                "The Black Keys ─ Walk Across The Water",
                "Ellie Goulding ─ Hate Me (with Juice WRLD)",
                "J Balvin ─ QUE PRETENDES",
                "Mustard ─ Ballin' (feat. Roddy Ricch)",
            ],
            "soundcloudLink": "https://soundcloud.com/edsheeran/beautiful-people-feat-khalid",
            "artworkLink": "https://i1.sndcdn.com/artworks-TtVL7y4jxVVz-0-large.jpg",
        }
        with self.assertRaises(BuggyLineException):
            self.genius_client.assert_valid_lines(test_invalid["lyrics"])
        test_invalid = {
            "song": "John Lennon ─ Imagine ─ Remastered 2010",
            "lyrics": [
                "— 01/01 : FOURBI ─ Fragments EP",
                "— 01/01 : Anna Pest ─ Dark Arms Reach Skyward With Bone White Fingers",
                "* 04/01 : FÉLIXE ─ Remixs",
                "* 08/01 : Firas Nassri ─ La Levantine",
                "* 08/01 : Treecy McNeil ─ Graffiti",
                "— 08/01 : Willows ─ The Hills",
            ],
            "soundcloudLink": "https://soundcloud.com/john-lennon-official/imagine-2010-remaster",
            "artworkLink": "https://i1.sndcdn.com/artworks-6ghV6sg5KE4u-0-large.jpg",
        }
        with self.assertRaises(BuggyLineException):
            self.genius_client.assert_valid_lines(test_invalid["lyrics"])

    def test_more_buggy_line(self):
        test_invalid = {
            "song": "The Rolling Stones ─ Brown Sugar ─ Remastered",
            "lyrics": [
                "Blanca — Shattered (2018)",
                'LouGotCash (feat. Trippie Redd) — "Too Turnt" (2018)October 4Terri Clark — Raising the Bar (2018)',
                'Jess Kent — "Girl" (2018)',
                "Joey Purp — QUARTERTHING (2018)",
                'Cypress Hill — "Crazy" (2018)',
                'Brooke Evers (feat. Rachel West & Glen Faria) — "Turn Around" (2018)',
            ],
            "soundcloudLink": "https://soundcloud.com/rolling-stones-official/brown-sugar-live-2009-re",
            "artworkLink": "https://i1.sndcdn.com/artworks-9HUkK7fafvlr-0-large.jpg",
        }
        with self.assertRaises(BuggyLineException):
            self.genius_client.assert_valid_lines(test_invalid["lyrics"])

        with self.assertRaises(BuggyLineException):
            self.genius_client.assert_valid_lines(test_invalid["lyrics"])

    def test_assert_valid_lines_when_clean(self):
        test_valid = {
            "song": "5SOS ─ Want You Back",
            "lyrics": [
                "Can't help but wondering if this",
                "Is the last time that I'll see your face",
                "Is it tears or just the fucking rain?",
                "Wish I could say something",
                "Something that doesn't sound insane",
                "But lately, I don't trust my brain",
            ],
            "soundcloudLink": "https://soundcloud.com/5sos3/5sos-want-you-back",
            "artworkLink": "https://i1.sndcdn.com/artworks-000308893377-sadj4w-large.jpg",
        }

        self.genius_client.assert_valid_lines(test_valid["lyrics"])


if __name__ == "__main__":
    unittest.main()

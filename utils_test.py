from lyricle import Lyricle
from utils import TypeScriptSeralizer
import unittest
import re

from utils import LyricleJSONSerializer


class TestTypeScriptSeralizer(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_json = """
            "lyrics": [
                "Today is gonna be the day that they're gonna throw it back to you",
                "By now, you shoulda somehow realised what you gotta do",
                "I don't believe that anybody feels the way I do about you now",
                "Backbeat, the word is on the street that the fire in your heart is out",
                "I'm sure you've heard it all before, but you never really had a doubt",
                "I don't believe that anybody feels the way I do about you now"
            ],
            "song": "Oasis ─ Wonderwall"
        },
            {
            "lyrics": [
                "Morgan v. Hennigan, U.S. District Court for Massachusetts, 1974",
                "THE SEEK BUTTON on the Ford's radio is working. The downtown recedes. Miles of neighborhoods fill the windshield. The SEEK function locks on someplace in stereo, college FM probably. \"Yeah,\" a new friend says, \"Whas up. Whas goin on.\" The radio has another button, VOL, which gets jacked repeatedly while the Ford hurtles, happily, to the source of the noise. Not to the station's broadcast booth on a campus across the river, nor to its transmission towers in the suburbs, but rather to RJam Productions in North Dorchester, where black kids from Boston's now-integrated high schools-Latin, Madison Park, Jeremiah Burke, Mattapan-cut demos and dream of being bigger than even the radio's new friend, a young man named Schoolly D who right now, at speaker-damaging volume, sounds darn big. \"Before we start this next record…,\" Schooly's saying. The record in question is called \"Signifying Rapper,\" a brief, bloody tale of ghetto retribution from Side 2 of Schoolly's Smoke Some Kill.",
                "The black areas are cut away from the white areas a federal judge ruled in '74, and evidence is everywhere that nothing's changed since then. On the southbound left of the Fitzgerald Expressway pass 20 blocks of grim Irish-Catholic housing projects, the western border of Belfast, complete with Sinn Fein graffiti and murals depicting a glorious United Ireland, a neighborhood where the gadfly will get his fibula busted for praising the '74 court order that bused \"Them\" from wherever it is \"They\" live-the Third World fer crissakes--into 97-percent-white South Boston. On the Expressway's right is the place the fibula-busters are talking about: the simultaneous northern border of Haiti, Jamaica and Georgia; a territory that maps of Boston call North Dorchester.",
                "Uniting the two sides of the Expressway is just about nothing. Both neighborhoods are tough and poor. Both hate the college world across the river, which, because of Boston's rotten public schools, they will never see as freshmen. And kids from both neighborhoods can do this hating to the beat of undergraduate radio, which this fine morning features suburban kids with student debt broadcasting the art of a ghetto Philadelphian roughly their age, once much poorer than they, but now, on royalties from Smoke Some Kill, very much richer.",
                "Not that the shared digging of black street music is news, or even new: twenty years ago, when Morgan v. Hennigan, Boston's own Brown v. Board of Education, was inching through the courts, and even dark-complected Italians were sometimes unwelcome in the Irish precincts east of the Expressway, kids in Boston's Little Belfast sang along with James Brown over the radio.",
                "\"Say it loud"
            ],
            "song": "U2 ─ With Or Without You - Remastered"
        }"""

    def test_to_string_with_two_props(self):
        corrected_lyrics = TypeScriptSeralizer.to_string(self.test_json)
        for prop in TypeScriptSeralizer.field_properties:
            pattern = re.compile(f'"{prop}"')
            self.assertNotRegex(corrected_lyrics, pattern)

    def test_to_string_with_four_props(self):
        test_song = """{
            lyrics: [
                'Tell me something I need to know',
                'Then take my breath and never let it go',
                'If you just let me invade your space',
                'I’ll take the pleasure, take it with the pain',
                'And if in the moment, I bite my lip',
                'Baby, in that moment, you’ll know this is',
            ],
            song: 'Ariana Grande ─ Love Me Harder',
            "soundcloudLink": 'https://soundcloud.com/arianagrande/love-me-harder',
            artworkLink: 'https://i1.sndcdn.com/artworks-VwczzbQomfJ7-0-large.jpg',
        }"""
        corrected_lyrics = TypeScriptSeralizer.to_string(test_song)
        for prop in TypeScriptSeralizer.field_properties:
            pattern = re.compile(f'"{prop}"')
            self.assertNotRegex(corrected_lyrics, pattern)


class TestLyricleJSONSerializer(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.result = Lyricle.generate_lyricles_from_playlist(
            "5Rrf7mqN8uus2AaQQQNdc1", limit=5
        )

    def test_generate_song_choices_from_data(self):
        LyricleJSONSerializer.generate_song_list_from_data(self.result)

    def test_generate_valid_guesses_from_data(self):
        LyricleJSONSerializer.generate_valid_guesses_from_data(self.result)

    def test_to_json(self):
        result = LyricleJSONSerializer.generate_valid_guesses_from_data(self.result)

        LyricleJSONSerializer.to_json(result, "test.json")


if __name__ == "__main__":
    unittest.main()

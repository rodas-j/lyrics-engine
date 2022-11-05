import unittest
from unittest import mock
import lyrics

response = '{"result":[{"song":"Hello","song-link":"https:\/\/www.lyrics.com\/lyric\/33637964\/Adele\/Hello","artist":"Adele","artist-link":"https:\/\/www.lyrics.com\/artist\/Adele\/861756","album":"Grammy Nominees 2017","album-link":"https:\/\/www.lyrics.com\/album\/3433278\/Grammy Nominees 2017"},{"song":"Hello","song-link":"https:\/\/www.lyrics.com\/lyric\/33681885\/Adele\/Hello","artist":"Adele","artist-link":"https:\/\/www.lyrics.com\/artist\/Adele\/861756","album":"Grammy Nominees 2017","album-link":"https:\/\/www.lyrics.com\/album\/3453244\/Grammy Nominees 2017"},{"song":"Hello","song-link":"https:\/\/www.lyrics.com\/lyric\/32298025\/Adele\/Hello","artist":"Adele","artist-link":"https:\/\/www.lyrics.com\/artist\/Adele\/861756","album":"25 [LP]","album-link":"https:\/\/www.lyrics.com\/album\/3273097\/25 [LP]"},{"song":"Hello","song-link":"https:\/\/www.lyrics.com\/lyric\/32298027\/Adele\/Hello","artist":"Adele","artist-link":"https:\/\/www.lyrics.com\/artist\/Adele\/861756","album":"25","album-link":"https:\/\/www.lyrics.com\/album\/3273098\/25"},{"song":"Hello","song-link":"https:\/\/www.lyrics.com\/lyric\/32307506\/Adele\/Hello","artist":"Adele","artist-link":"https:\/\/www.lyrics.com\/artist\/Adele\/861756","album":"25","album-link":"https:\/\/www.lyrics.com\/album\/3273098\/25"},{"song":"Hello","song-link":"https:\/\/www.lyrics.com\/lyric\/34061027\/Adele\/Hello","artist":"Adele","artist-link":"https:\/\/www.lyrics.com\/artist\/Adele\/861756","album":"Grammy Nominees 2017","album-link":"https:\/\/www.lyrics.com\/album\/3474606\/Grammy Nominees 2017"}]}'

hello = """Hello, it's me
I was wondering if after all these years you'd like to meet
To go over everything
They say that time's supposed to heal ya
But I ain't done much healing

Hello, can you hear me?
I'm in California dreaming about who we used to be
When we were younger and free
I've forgotten how it felt before the world fell at our feet

There's such a difference between us
And a million miles

Hello from the other side
I must've called a thousand times
To tell you I'm sorry
For everything that I've done
But when I call you never
Seem to be home

Hello from the outside
At least I can say that I've tried
To tell you I'm sorry
For breaking your heart
But it don't matter, it clearly
Doesn't tear you apart anymore

Hello, how are you?
It's so typical of me to talk about myself, I'm sorry
I hope that you're well
Did you ever make it out of that town
Where nothing ever happened?

It's no secret
That the both of us
Are running out of time

So hello from the other side (other side)
I must've called a thousand times (thousand times)
To tell you I'm sorry
For everything that I've done
But when I call you never
Seem to be home

Hello from the outside (outside)
At least I can say that I've tried (I've tried)
To tell you I'm sorry
For breaking your heart
But it don't matter, it clearly
Doesn't tear you apart anymore

Oh, anymore
Oh, anymore
Oh, anymore
Anymore

Hello from the other side (other side)
I must've called a thousand times (thousand times)
To tell you I'm sorry
For everything that I've done
But when I call you never
Seem to be home

Hello from the outside (outside)
At least I can say that I've tried (I've tried)
To tell you I'm sorry
For breaking your heart
But it don't matter, it clearly
Doesn't tear you apart anymore"""


class TestLyrics(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        # MockLyrics = mock.patch("lyrics.Lyrics").start()
        lyrics.Lyrics.get_request_lyrics = mock.MagicMock()
        lyrics.Lyrics.parse_lyrics = mock.MagicMock()
        lyrics.Lyrics.parse_lyrics.return_value = hello
        MockResponse = mock.MagicMock()

        MockResponse.text = response
        lyrics.Lyrics.get_request_lyrics.return_value = MockResponse
        # MockLyrics.return_value = m
        # self.addCleanup(mock.patch.stopall())

    def test_hello(self):
        lyric = lyrics.Lyrics("Hello", "Adele")
        self.assertEqual(lyric.artist, "Adele")
        self.assertEqual(lyric.title, "Hello")

    def test_to_json(self):
        lyric = lyrics.Lyrics("Hello", "Adele")
        expected = {
            "title": "Hello",
            "artist": "Adele",
            "lyrics": [
                "Hello, it's me",
                "I was wondering if after all these years you'd like to meet",
                "To go over everything",
                "They say that time's supposed to heal ya",
                "But I ain't done much healing",
                "Hello, can you hear me?",
                "I'm in California dreaming about who we used to be",
                "When we were younger and free",
                "I've forgotten how it felt before the world fell at our feet",
                "There's such a difference between us",
                "And a million miles",
                "Hello from the other side",
                "I must've called a thousand times",
                "To tell you I'm sorry",
                "For everything that I've done",
                "But when I call you never",
                "Seem to be home",
                "Hello from the outside",
                "At least I can say that I've tried",
                "To tell you I'm sorry",
                "For breaking your heart",
                "But it don't matter, it clearly",
                "Doesn't tear you apart anymore",
                "Hello, how are you?",
                "It's so typical of me to talk about myself, I'm sorry",
                "I hope that you're well",
                "Did you ever make it out of that town",
                "Where nothing ever happened?",
                "It's no secret",
                "That the both of us",
                "Are running out of time",
                "So hello from the other side (other side)",
                "I must've called a thousand times (thousand times)",
                "To tell you I'm sorry",
                "For everything that I've done",
                "But when I call you never",
                "Seem to be home",
                "Hello from the outside (outside)",
                "At least I can say that I've tried (I've tried)",
                "To tell you I'm sorry",
                "For breaking your heart",
                "But it don't matter, it clearly",
                "Doesn't tear you apart anymore",
                "Oh, anymore",
                "Oh, anymore",
                "Oh, anymore",
                "Anymore",
                "Hello from the other side (other side)",
                "I must've called a thousand times (thousand times)",
                "To tell you I'm sorry",
                "For everything that I've done",
                "But when I call you never",
                "Seem to be home",
                "Hello from the outside (outside)",
                "At least I can say that I've tried (I've tried)",
                "To tell you I'm sorry",
                "For breaking your heart",
                "But it don't matter, it clearly",
                "Doesn't tear you apart anymore",
            ],
        }
        self.assertDictEqual(lyric.to_json(), expected)


if __name__ == "__main__":
    unittest.main()

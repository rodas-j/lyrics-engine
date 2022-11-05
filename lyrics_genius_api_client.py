import lyricsgenius
import re
import os

from soundcloud_api_client import SongDoesntExistError
from lyric_linter import LyricLinter


class WrongLyricsException(Exception):
    pass


class LyricsStateNotComplete(Exception):
    pass


class BuggyLineException(Exception):
    pass


class LyricsGeniusAPIClient:
    TOKEN = os.environ.get("GENIUS_TOKEN")
    MAX_LIMIT = 0

    def __init__(self):
        self.genius = lyricsgenius.Genius(LyricsGeniusAPIClient.TOKEN)
        self.genius.remove_section_headers = True
        self.genius.retries = (
            3  # THE GENIUS API SOMETIMES FAILS SO I SET THE RETRY TO 3
        )
        self.limit = 6

    def get_lyrics(self, song_name, artist_name):
        song = self.genius.search_song(song_name, artist_name)

        if song == None:
            raise NameError(f"Song Not Found: {song_name} by {artist_name}")
        if not self.is_valid_song(song, artist_name):
            raise SongDoesntExistError(
                f"This song ({song_name} by {artist_name}) doesn't exist in Lyrics Genius."
            )
        lyrics = song.lyrics

        return lyrics

    def get_lyricle_list(self, song_name, artist):
        lyrics = self.get_lyrics(song_name, artist)
        pattern = "\d*Embed"
        lyrics_body = re.sub(pattern, "", lyrics)
        lyrics_lst = re.split("\n+", lyrics_body)
        titled_lyrics_lst = list(filter(("").__ne__, lyrics_lst))
        no_title_lyrics_lst = titled_lyrics_lst[1:]
        if self.limit == 0:
            return no_title_lyrics_lst
        # * LYRIC LINTING
        filtered_lst = LyricLinter(
            no_title_lyrics_lst, song_name).get_linted_lyrics()
        portioned_lst = filtered_lst[: self.limit]
        # TODO Find better position for this.
        self.assert_valid_lines(portioned_lst)
        return portioned_lst

    def assert_valid_lines(self, portioned_lst):

        pattern = re.compile(".* [—─-] .*")
        for line in portioned_lst:
            if re.match(pattern, line):
                raise BuggyLineException(
                    f"Lyrics line has the pattern '.* ─ .*' {line}"
                )

    def is_valid_song(self, song_obj, artist):
        if artist.lower().strip() not in song_obj.artist.lower().strip():
            return False
        if song_obj.lyrics_state != "complete":
            raise LyricsStateNotComplete(
                f"The Lyrics State is : {song_obj.lyrics_state}"
            )
        return True

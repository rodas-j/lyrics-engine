from datetime import datetime
import logging
import re
from lyrics_genius_api_client import BuggyLineException, LyricsGeniusAPIClient
from model import SongData
from soundcloud_api_client import SongDoesntExistError, SoundCloudAPIClient
from spotify_api_client import SpotifyAPIClient
from lyricscom import lyrics


today = datetime.today().date().isoformat()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    filename=f"logs/{today}.log",
    filemode="a",
)


class Lyricle:
    @staticmethod
    def generate_lyricles_from_playlist(playlist, limit=0):
        tracks = SpotifyAPIClient.get_song_tuples_from_playlist(
            playlist
        )  # [(song_name, artist_name)...]
        result = []
        if limit == 0:
            limit = len(tracks) - 1
        skipped = []
        for track in tracks[:limit]:
            cleaned = SpotifyAPIClient.clean_tags(track[0])
            try:
                song_data = Lyricle.generate_lyricle(cleaned, track[1])
            except:
                skipped.append(" by ".join(track))
                continue
            result.append(song_data)
        lst = "\n".join(skipped)
        logging.info(
            f"{len(skipped)} out of {limit+1} songs were skipped. Playlist ID: {playlist}"
        )
        logging.info(f"Skipped Songs:\n{lst}")
        return result

    @staticmethod
    def generate_lyricles_from_txt(text_file_path, limit=0):
        tracks = []
        with open(text_file_path) as fp:
            lines = fp.readlines()
        for line in lines:
            (title, artist) = line.split("_")
            track = SpotifyAPIClient.search_track(title, artist)
            tracks.append(track)
        result = []
        if limit == 0:
            limit = len(tracks) - 1
        skipped = []
        for track in tracks[:limit]:
            cleaned = SpotifyAPIClient.clean_tags(track["title"])
            try:
                song_data = Lyricle.generate_lyricle(cleaned, track["artist"])
            except:
                skipped.append(" by ".join(track))
                continue
            result.append(song_data)
        lst = "\n".join(skipped)
        logging.info(
            f"{len(skipped)} out of {limit+1} songs were skipped. Song Text File: {text_file_path}"
        )
        logging.info(f"Skipped Songs:\n{lst}")
        return result

    @staticmethod
    def generate_lyricle(song_name, artist_name):
        json_response = {}
        soundcloud_client = SoundCloudAPIClient()
        try:
            souncloud_respose = soundcloud_client.get_verified_song(
                SpotifyAPIClient.clean_tags(song_name), artist_name
            )

        except SongDoesntExistError as e:
            logging.warning(str(e))
            song_name = re.sub(" [─-─] .*", "", song_name)
            logging.info(f"Trying {song_name} instead.")
            try:
                souncloud_respose = soundcloud_client.get_verified_song(
                    song_name, artist_name
                )

            except:
                logging.warning(f"Failed to find song: {song_name}")
                raise SongDoesntExistError(
                    f"Failed to find song {song_name} by {artist_name}."
                )
        except BuggyLineException:
            logging.info(
                f"{song_name} by {artist_name} doesn't exist in Lyrics Genius."
            )

        artwork_url = souncloud_respose["artwork_url"]
        if not soundcloud_client.is_valid_link(souncloud_respose["permalink_url"]):
            raise Exception("The soundcloud link is broken")
        soundcloud_link = souncloud_respose["permalink_url"]
        try:
            song_lyrics = lyrics.Lyrics(song_name, artist_name)
        except NameError:
            logging.warning(f"{song_name} by {artist_name} was not found.")
            song_name = re.sub(" - .*", "", song_name)
            logging.info(f"Trying {song_name} instead.")
            song_lyrics = lyrics.Lyrics(song_name, artist_name)
        except BuggyLineException:
            logging.warning(
                f"{song_name} by {artist_name} has a buggy line. Trying again"
            )
            song_lyrics = lyrics.Lyrics(song_name, artist_name)

        lyricle = SongData(
            title=song_name.strip(),
            artist=artist_name.strip(),
            lyrics=song_lyrics.to_json()["lyrics"][:8],
            songLink=soundcloud_link,
            artworkLink=artwork_url,
        )

        return lyricle

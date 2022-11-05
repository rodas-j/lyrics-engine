""" 
Lyricle Song Generator
Author: Rodas Jateno (rodas-j)
"""
from datetime import datetime
import json
import logging
import re
import random
from absl import app, flags
from attr import asdict
from lyricle import Lyricle
from lyrics_genius_api_client import BuggyLineException, LyricsGeniusAPIClient
from soundcloud_api_client import SongDoesntExistError, SoundCloudAPIClient
from spotify_api_client import SpotifyAPIClient
from utils import LyricleJSONSerializer, TypeScriptSeralizer

today = datetime.today().date().isoformat()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    filename=f"logs/{today}.log",
    filemode="a",
)


FLAGS = flags.FLAGS
flags.DEFINE_string("title", None, "Song Title")
flags.DEFINE_string("artist", None, "Song Artist")
flags.DEFINE_string("playlist_id", None, "Playlist ID")
flags.DEFINE_string("output", None, "File Output")
flags.DEFINE_string("path", None, "Text File Path")
flags.DEFINE_bool("include", False, "Include as valid guess")

# Mutually Exclusive Flags

flags.mark_flags_as_mutual_exclusive(
    ["title", "playlist_id", "path"], required=True)
flags.mark_flags_as_mutual_exclusive(
    ["artist", "playlist_id", "path"], required=True)


def get_song_lyricle(title, artist, include):
    try:
        track = SpotifyAPIClient.search_track(title, artist)
        song_data = Lyricle.generate_lyricle(
            track["title"], track["artist"].split(", ")[0]
        )
        song_data.artist = track["artist"]

        if include:

            with open("out/all_validGuesses.json", "r") as f:
                initial_valid_guesses = json.load(f)
            LyricleJSONSerializer.generate_song_list_from_data
            valid_guesses = LyricleJSONSerializer.append_valid_guesses(
                initial_valid_guesses,
                LyricleJSONSerializer.generate_song_list_from_data([
                                                                   song_data]),
            )
            LyricleJSONSerializer.to_json_file(
                valid_guesses, f"all_validGuesses.json")

    except SongDoesntExistError:
        raise SongDoesntExistError(
            f"Song {title} doesn't exist for the artist {artist} please correct your input."
        )
    except:
        print("Something went wrong. Please try again.")
        raise

    json_string = LyricleJSONSerializer.to_json(song_data)

    return json_string


def main(argv):
    del argv  # Unused.

    if FLAGS.playlist_id is not None:
        song_data_list = Lyricle.generate_lyricles_from_playlist(
            FLAGS.playlist_id)
        song_choices = LyricleJSONSerializer.generate_song_list_from_data(
            song_data_list
        )
        valid_guesses = LyricleJSONSerializer.generate_valid_guesses_from_data(
            song_data_list
        )

        if FLAGS.output is not None:
            LyricleJSONSerializer.to_json_file(
                song_choices, f"{FLAGS.output}.json")
            LyricleJSONSerializer.to_json_file(
                valid_guesses, f"{FLAGS.output}_validGuesses.json"
            )
            return
        if len(song_choices) < 10:
            print(song_choices)
        return

    if FLAGS.path is not None:
        song_data_list = Lyricle.generate_lyricles_from_txt(FLAGS.path, 6)
        song_choices = LyricleJSONSerializer.generate_song_list_from_data(
            song_data_list
        )
        valid_guesses = LyricleJSONSerializer.generate_valid_guesses_from_data(
            song_data_list
        )

        if FLAGS.output is not None:
            LyricleJSONSerializer.to_json_file(
                song_choices, f"{FLAGS.output}.json")
            LyricleJSONSerializer.to_json_file(
                valid_guesses, f"{FLAGS.output}_validGuesses.json"
            )
            return
    json_string = get_song_lyricle(FLAGS.title, FLAGS.artist, FLAGS.include)

    print(json_string)


if __name__ == "__main__":
    app.run(main)

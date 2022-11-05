from dataclasses import dataclass, asdict
import json
import re
from secrets import choice
from slugify import slugify

from model import SongChoice, ValidGuesses


class TypeScriptSeralizer:

    field_properties = ["song", "lyrics", "soundcloudLink", "artworkLink"]

    @staticmethod
    def to_string(json_formatted_string):
        for prop in TypeScriptSeralizer.field_properties:
            json_formatted_string = re.sub(
                f'"{prop}"', f"{prop}", json_formatted_string
            )
        return json_formatted_string

    @staticmethod
    def decorate(lst_of_json_objs):
        result = []
        for json_obj in lst_of_json_objs:
            json_string = json.dumps(json_obj, ensure_ascii=False)
            json_string = re.sub(
                " - ", " ─ ", json_string
            )  # To match validGuesses format
            ts_string = TypeScriptSeralizer.to_string(json_string)
            result.append(ts_string)

        return ",".join(result)


# class LyricleJSONSerializer:
#     @staticmethod
#     def generate_song_choices_from_data(song_data):
#         choices = []
#         for song in song_data:
#             song_id = song.title + song.artist
#             song_id = slugify(song_id, separator="")
#             song_choice = SongChoice(song_id=song_id, data=song)
#             choices.append(song_choice)
#         return choices

#     def generate_valid_guesses_from_data(song_data):
#         guesses = []
#         for song in song_data:
#             song_id = song.title + song.artist
#             song_id = slugify(song_id, separator="")
#             valid_guess = ValidGuesses(
#                 song_id=song_id, title=song.title, artist=song.artist
#             )
#             guesses.append(valid_guess)
#         return guesses

#     @staticmethod
#     def to_json(data_list, file_name):
#         json_output = []
#         for data in data_list:
#             json_output.append(asdict(data))
#         output = json.dumps(json_output, ensure_ascii=False)
#         with open(f"out/{file_name}", mode="w") as f:
#             f.write(output)

#     @staticmethod
#     def to_json(song_data):
#         return json.dumps(asdict(song_data), ensure_ascii=False)


class LyricleJSONSerializer:
    @staticmethod
    def generate_song_list_from_data(song_data_list):
        choices = []
        for song_data in song_data_list:
            choices.append(asdict(song_data))

        return choices

    @staticmethod
    def append_valid_guesses(initial_valid_guesses, new_valid_guesses):
        catalog = set()
        for guess in initial_valid_guesses:
            for title in guess["songs"]:
                catalog.add((title, guess["artist"]))

        for lyricle in new_valid_guesses:
            title = lyricle["title"]
            artist = lyricle["artist"]
            if (title, artist) not in catalog:
                found = False
                for i, search in enumerate(initial_valid_guesses):
                    if search["artist"] == artist:
                        found = True
                        initial_valid_guesses[i]["songs"].append(title)
                        break
                if not found:
                    initial_valid_guesses.append({"artist": artist, "songs": [title]})
                catalog.add((title, artist))

        return initial_valid_guesses

    def generate_valid_guesses_from_data(song_data):
        valid_guesses = []
        LyricleJSONSerializer.append_valid_guesses(
            valid_guesses, LyricleJSONSerializer.generate_song_list_from_data(song_data)
        )
        return valid_guesses

    @staticmethod
    def to_json_file(data_list, file_name):

        output = json.dumps(data_list, ensure_ascii=False)
        with open(f"out/{file_name}", mode="w") as f:
            f.write(output)

    @staticmethod
    def to_json(song_data):
        return json.dumps(asdict(song_data), ensure_ascii=False)

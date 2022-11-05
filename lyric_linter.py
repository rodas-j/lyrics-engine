import re
import string
import pandas as pd
from offensive_words import offensive_words
from fuzzywuzzy import fuzz


class LyricLinter:
    def __init__(self, lyrics, title):
        self.lyrics = lyrics
        self.title = title
        self.filler_prob = (
            0.33  # % of repeated word in lyric needed to label a line filler
        )
        # % of repeated line in lyric[i:fov] makes it filler
        self.line_repeat_prob = 0.24
        self.fov = 8  # no of lines in section to be scanned for repeated words

    @staticmethod  # Removes punctuations and turns all letters to lowercase
    def get_formatted_string(s):
        if len(s) > 5 and s[-3] == "x" and s[-2].isnumeric():
            s = s[:-5]
        return s.lower().translate(str.maketrans("", "", string.punctuation))

    @staticmethod
    def remove_cover_songs(song_list):
        index_of_songs_to_be_removed = []
        for i in range(len(song_list)):
            for j in range(i + 1, len(song_list)):
                if i == j:
                    continue
                elif (
                    fuzz.token_set_ratio(song_list[i].lyrics, song_list[j].lyrics) > 90
                    and i not in index_of_songs_to_be_removed
                ):
                    index_of_songs_to_be_removed.append(j)

        balancer = 0
        for i in index_of_songs_to_be_removed:
            song_list.pop(i - balancer)
            balancer += 1
        return song_list

    def fold_lines(self, index):
        # if previous i has x
        if self.lyrics[index - 1][-3] == "x" and self.lyrics[index - 1][-2].isnumeric():
            # increament by one
            self.lyrics[index - 1] = (
                self.lyrics[index - 1][:-2]
                + str(int(self.lyrics[index - 1][-2]) + 1)
                + ")"
            )
        # else
        else:
            # add x2
            self.lyrics[index - 1] += " (x2)"

    def fold_line(self, line_index, word_index):
        if (
            self.lyrics[line_index][word_index - 1][-3] == "x"
            and self.lyrics[line_index][word_index - 1][-2].isnumeric()
        ):
            self.lyrics[line_index][word_index - 1] = (
                self.lyrics[line_index][word_index - 1][:-2]
                + str(int(self.lyrics[line_index][word_index - 1][-2]) + 1)
                + ")"
            )
        else:
            self.lyrics[line_index][word_index - 1] += " (x2)"

    def lint_line_in_repeated_section(self):
        lyrics_len = len(self.lyrics)
        j = 0
        while (j + self.fov) < lyrics_len:
            line_count = {}
            # loop over `FOV` lines
            for i, line in enumerate(self.lyrics[j : j + self.fov]):
                line = self.get_formatted_string(line)
                # get line count of fov lines
                if line not in line_count.keys():
                    line_count[line] = {"count": 1, "indices": []}
                    continue

                line_count[line]["count"] += 1
                line_count[line]["indices"].append(j + i)

            # loop over word_counr
            for i in line_count.keys():
                # check if line count is greater than 33%
                if (line_count[i]["count"] / self.fov) > self.line_repeat_prob:
                    balancer = 0
                    for k in line_count[i]["indices"]:
                        # remove lyric line index
                        self.lyrics.pop(k - balancer)
                        # decrement j
                        j -= 1
                        balancer += 1
                        # decrement lyrics_len
                        lyrics_len -= 1

            j += self.fov - 1

    def lint_filler_words(self):
        lyrics_len = len(self.lyrics)
        j = 0
        while j < lyrics_len:
            word_count = {}
            filler = False
            for i in self.lyrics[j].split():
                i = self.get_formatted_string(i)
                word_count[i] = word_count[i] + 1 if i in word_count.keys() else 1

            for i in word_count.keys():
                # Check if % of word in line is greater than the filler probability
                if (word_count[i] / sum(word_count.values())) > self.filler_prob:
                    # pop filler line j in lyric
                    self.lyrics.pop(j)
                    # decrease j by 1 bc the current i has been popped
                    j -= 1
                    # decrease len of lyrics by 1
                    lyrics_len -= 1
                    # break loop
                    break

            j += 1

    def lint_repeated_words(self):
        # loop through lines
        for i in range(len(self.lyrics)):
            self.lyrics[i] = self.lyrics[i].split()
            # set len of line
            len_line = len(self.lyrics[i])
            j = 1
            # loop through words
            while j < len_line:
                # if word is a single letter skip
                # if len(self.lyrics[i][j]) < 3:
                #     j += 1
                #     continue

                # if previous word has x
                if len(self.lyrics[i][j - 1]) < 3:
                    prev_word = self.lyrics[i][j - 1]
                elif (
                    self.lyrics[i][j - 1][-3] == "x"
                    and self.lyrics[i][j - 1][-2].isnumeric()
                ):
                    prev_word = self.lyrics[i][j - 1][:-5]
                else:
                    prev_word = self.lyrics[i][j - 1]

                # check if word == previous word
                if self.get_formatted_string(
                    self.lyrics[i][j]
                ) == self.get_formatted_string(prev_word):
                    # append or increment x on previous word
                    self.fold_line(i, j)
                    # pop word
                    self.lyrics[i].pop(j)
                    # decrement len of line
                    len_line -= 1
                    j -= 1

                j += 1

            self.lyrics[i] = " ".join(self.lyrics[i])

    def lint_short_lines(self):
        # set len of lyrics
        lyrics_len = len(self.lyrics) - 1
        i = 0
        # loop through lyrics
        while i < lyrics_len:
            # if previous i has x
            if len(self.lyrics[i].split()) < 4:
                self.lyrics[i] += " " + self.lyrics[i + 1]
                self.lyrics.pop(i + 1)
                # decrease len of lyrics by 1
                lyrics_len -= 1
            i += 1

    def lint_offensive_words(self):
        self.lyrics = "\n".join(self.lyrics)
        for ow in offensive_words:
            pattern = r"(?xi)" + r"\s".join(ow.split())
            self.lyrics = re.sub(
                pattern, ow[0].lower() + "*" * (len(ow) - 1), self.lyrics
            )
        self.lyrics = self.lyrics.split("\n")

        # for i in range(len(self.lyrics)):
        #     self.lyrics[i] = self.lyrics[i].capitalize()

    def lint_title_in_lyrics(self):
        for i in range(len(self.lyrics)):
            pattern = r"(?xi)" + r"\s".join(self.title.split())
            self.lyrics[i] = re.sub(
                pattern,
                self.title[0].lower() + "_" * (len(self.title) - 1),
                self.lyrics[i],
            )
            # self.lyrics[i] = self.lyrics[i].capitalize()

    def lint_repeated_lines(self):
        # set len of lyrics
        lyrics_len = len(self.lyrics)
        i = 0
        # loop through lyrics
        while i < lyrics_len:
            # if previous i has x
            if self.lyrics[i - 1][-3] == "x" and self.lyrics[i - 1][-2].isnumeric():
                # get the main lyric only
                prev_line = self.lyrics[i - 1][:-5]
            else:
                prev_line = self.lyrics[i - 1]

            # if previous i has x
            if self.lyrics[i][-3] == "x" and self.lyrics[i][-2].isnumeric():
                # get the main lyric only
                current_line = self.lyrics[i][:-5]
            else:
                current_line = self.lyrics[i]

            # if previous i equals i
            if (
                fuzz.token_set_ratio(
                    self.get_formatted_string(prev_line),
                    self.get_formatted_string(current_line),
                )
                > 98
            ):
                # fold line
                self.fold_lines(i)
                # pop current i
                self.lyrics.pop(i)
                # decrease i by 1 bc the current i has been popped
                i -= 1
                # decrease len of lyrics by 1
                lyrics_len -= 1
            i += 1

    def get_linted_lyrics(self):

        self.lint_filler_words()
        # self.lint_repeated_words()
        self.lint_repeated_lines()
        # self.lint_line_in_repeated_section()
        self.lint_short_lines()
        self.lint_offensive_words()
        # self.lint_title_in_lyrics()

        return self.lyrics

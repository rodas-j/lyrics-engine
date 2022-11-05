from ast import parse
import requests
import json
from bs4 import BeautifulSoup
import os


class Lyrics:
    def __init__(self, title, artist) -> None:
        self.get_lyrics(title, artist)

    def extract_songLink(self, response):
        # with open("test_data/alphaville.json") as f:
        #     response = json.loads(f.read())

        songLink = response["result"][0]["song-link"]
        return songLink

    def parse_lyrics(self, url):
        res = requests.request("GET", url)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.find("pre").text

    def get_request_lyrics(self, term, artist):
        url = f"https://www.stands4.com/services/v2/lyrics.php?uid=10651&tokenid={os.environ.get('LYRICS_TOKEN')}&term={term}&artist={artist}&format=json"

        payload = {}
        headers = {
            "Cookie": "AWSALB=7V1AFCxbKBR6omeUNoEJrOd0QzAHYjefXHMx1teTcUd0sx0cINTCw+54X5Ii5ZJWVEdkg4Pb+MH9ZnApcheKxeA1df5Fun2FC86YwD8ICXwyrZHwpT5mcGR/bYuW; AWSALBCORS=7V1AFCxbKBR6omeUNoEJrOd0QzAHYjefXHMx1teTcUd0sx0cINTCw+54X5Ii5ZJWVEdkg4Pb+MH9ZnApcheKxeA1df5Fun2FC86YwD8ICXwyrZHwpT5mcGR/bYuW"
        }
        return requests.request("GET", url, headers=headers, data=payload)

    def get_lyrics(self, term, artist):

        response = self.get_request_lyrics(term, artist)
        res = json.loads(response.text)
        lyrics = self.parse_lyrics(self.extract_songLink(res))
        self.lyrics = lyrics.replace("\r", "")
        self.title = res["result"][0]["song"]
        self.artist = res["result"][0]["artist"]
        return self

    @staticmethod
    def list_lyrics(lyrics_string):
        lst = lyrics_string.split("\n")
        return list(filter(lambda e: e != "", lst))

    def to_json(self):
        res = {}
        res["title"] = self.title
        res["artist"] = self.artist
        res["lyrics"] = Lyrics.list_lyrics(self.lyrics)
        return res


Lyrics("Hello", "Adele").lyrics

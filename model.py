import dataclasses
from typing import List


@dataclasses.dataclass
class SongData:
    title: str
    artist: str
    lyrics: List[str]
    songLink: str
    artworkLink: str


@dataclasses.dataclass
class SongChoice:
    song_id: str
    data: SongData


@dataclasses.dataclass
class ValidGuesses:
    song_id: str
    title: str
    artist: str

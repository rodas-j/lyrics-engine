# Lyrics Engine

Advanced Lyrics generating pipeline for Lyricle-like games. Given information about a song, it outputs a Lyricle: a six line lyrics of the song. The lyric lines should have enough characters for users to guess the song correctly.


# Getting Started
## Installing Requirements
```bash
pip install -r requirements.txt
```
## Creating .env file

Create a `.env` file and add two environment variables as follows:

```text
GENIUS_TOKEN="Lyrics Genius TOKEN"
LYRICS_TOKEN="Lyrics.com TOKEN"
SOUNDCLOUD_CLIENT_ID="Soundcloud.com CLIENT ID"
```

These TOKENS can be found on their respective official sites.

## Get Lyrics

The simple usecase would be to use it for one particular song and artist. 
```bash
python3 app.py --title="Hello" --artist="Adele"
```

### Get Lyrics from a Spotify Playlist

This functionality requires a playlist ID of any Spotify playlist. The ID can be found on the URL of any playlist link:

`https://open.spotify.com/playlist/<PLAYLIST_ID>`

```bash
python3 app.py --playlist_id="PLAYLIST_ID" --output="path/to/output"
```

The root directory for the output is out found in the root directory of the repo: `/out`.


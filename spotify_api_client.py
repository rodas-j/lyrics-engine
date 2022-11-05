import re
from spotipy import SpotifyClientCredentials, Spotify

from soundcloud_api_client import SongDoesntExistError

cid = "f9a2ddd688d54f57be9d2fc0c767057f"
secret = "7d3069b3636e489ab775ae546d4b71cb"
client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret
)
sp = Spotify(client_credentials_manager=client_credentials_manager)


class SpotifyAPIClient:
    @staticmethod
    def get_playlist_tracks(playlist_id):
        results = sp.playlist_tracks(playlist_id)
        tracks = results["items"]
        while results["next"]:
            results = sp.next(results)
            tracks.extend(results["items"])
        return tracks

    @staticmethod
    def get_song_tuples_from_playlist(playlist_id):
        tracks = SpotifyAPIClient.get_playlist_tracks(playlist_id)
        result_tuples = []
        for track in tracks:
            song_name = track["track"]["name"]
            artist_name = ", ".join(
                list(map(lambda x: x["name"], track["track"]["artists"]))
            )
            result_tuples.append((song_name, artist_name))
        return result_tuples

    @staticmethod
    def search_track(title, artist):
        q = f"{artist} {title}"
        results = sp.search(q, type="track", limit=1)
        if len(results["tracks"]["items"]) == 0:
            raise SongDoesntExistError(
                f"Unable to identify the song on Spotify. {title} by {artist}"
            )
        track = results["tracks"]["items"][0]
        name = track["name"]
        artist = ", ".join(list(map(lambda x: x["name"], track["artists"])))
        return {"title": SpotifyAPIClient.clean_tags(name), "artist": artist}

    def clean_tags(title):
        title = re.sub(" [─-] .*", "", title)
        title = re.sub("[─-─]\s*\d*\s*[Rr]emaster(ed)?.*", "", title)
        title = re.sub("\W?\(.*\)", "", title)
        title = re.sub("[─-─].*", "", title)
        return title

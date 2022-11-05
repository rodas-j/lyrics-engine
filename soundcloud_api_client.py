from pydoc import resolve
import requests
from requests.adapters import HTTPAdapter, Retry


class SongDoesntExistError(Exception):
    pass


class SoundCloudAPIClient:
    BASE_URL = "https://api-widget.soundcloud.com/"
    RESOLVE_ATTRIBUTE = "resolve"
    SEARCH_ATTRIBUTE = "search"
    CLIENT_ID = "LBCcHmRB8XSStWL6wKH2HPACspQlXg2P"

    def __init__(self):
        self.session = requests.Session()

        retries = Retry(
            total=10,
            backoff_factor=0.1,
            status_forcelist=[403, 429, 500, 502, 503, 504],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def search(self, query, limit=10, offset=0):
        search_url = (
            SoundCloudAPIClient.BASE_URL + SoundCloudAPIClient.SEARCH_ATTRIBUTE
        )
        query_parameters = {
            "q": query,
            "limit": limit,
            "offset": offset,
            "client_id": SoundCloudAPIClient.CLIENT_ID,
        }
        response = self.session.get(
            url=search_url, params=query_parameters, allow_redirects=True
        )
        response.raise_for_status()
        return response.json()

    def get_first_song(self, query):
        search_result = self.search(query, limit=20)
        if "collection" in search_result:
            if len(search_result["collection"]) != 0:
                return search_result["collection"][0]

        raise SongDoesntExistError(f"Unable to obtain song from query: {query}")

    def get_verified_song(self, song_name, artist_name):
        query = " ".join((artist_name, song_name))
        search_result = self.search(query, limit=20)
        if "collection" in search_result:
            if len(search_result["collection"]) != 0:
                filtered_result = self.filter_verified_songs(
                    artist_name, search_result["collection"]
                )
                if len(filtered_result) != 0:
                    return filtered_result[0]
        raise SongDoesntExistError(
            f"No Verified Song Found for {song_name} by {artist_name}"
        )

    def filter_verified_songs(self, artist_name, search_result):
        filtered_lst = []
        try:
            for result in search_result:
                if "user" in result:
                    if "username" in result["user"]:
                        if artist_name.lower().replace(" ", "") in result[
                            "user"
                        ]["username"].lower().replace(" ", ""):
                            filtered_lst.append(result)
        except KeyError as e:
            print(search_result)
            raise Exception(e)

        return filtered_lst

    def get_song_from_url(self, url):

        resolve_url = (
            SoundCloudAPIClient.BASE_URL + SoundCloudAPIClient.RESOLVE_ATTRIBUTE
        )
        query_parameters = {
            "url": url,
            "format": "json",
            "client_id": SoundCloudAPIClient.CLIENT_ID,
        }
        response = self.session.get(
            url=resolve_url, params=query_parameters, allow_redirects=True
        )
        response.raise_for_status()
        return response.json()

    def is_valid_link(self, url):

        search_url = (
            SoundCloudAPIClient.BASE_URL + SoundCloudAPIClient.RESOLVE_ATTRIBUTE
        )
        query_parameters = {
            "url": url,
            "client_id": SoundCloudAPIClient.CLIENT_ID,
        }
        response = self.session.get(
            url=search_url, params=query_parameters, allow_redirects=True
        )

        return response.status_code != 404

    def get_artwork_url_from_url(self, url):
        if self.get_song_from_url(url)["artwork_url"]:
            return self.get_song_from_url(url)["artwork_url"]
        else:
            raise KeyError("Artwork URL Doesn't Exist")

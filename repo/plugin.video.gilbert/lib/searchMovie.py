from path_config import configure_paths
configure_paths()
import requests

PROWLARR_API_KEY = "b388dd88c9f84cf1ba90123cef20b6b2"
PROWLARR_URL = "http://prowlarr.inter-datum.com"

def search_movie(movie_title):
    """
    Search for a movie in Prowlarr and return NZB details.

    :param movie_title: Title of the movie to search.
    :type movie_title: str
    :return: List of NZB search results.
    :rtype: list
    """
    url = f"{PROWLARR_URL}/search"
    headers = {"X-Api-Key": PROWLARR_API_KEY}
    params = {"query": movie_title}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to search movie: {response.status_code} - {response.text}")

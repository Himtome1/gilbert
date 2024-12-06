
from path_config import configure_paths
configure_paths()
import requests
def getGenres():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyY2JjZTU1OTRkMGVhZGFhZGM2Zjc5MmMyZmNjMDBhNiIsIm5iZiI6MTczMzIyNzMyOS4yNzYsInN1YiI6IjY3NGVmMzQxOTAyOWExZmNjMzZhYTY3ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.63qr-srVzSjCWOUpdktfYuBm-Wq29onvJ7dURjDElpU"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data['genres']
    
    else:
        return []

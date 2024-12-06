from path_config import configure_paths
configure_paths()
import requests

def getVideos(genre,page):
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page="+page+"&sort_by=popularity.desc&with_genres="+genre

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyY2JjZTU1OTRkMGVhZGFhZGM2Zjc5MmMyZmNjMDBhNiIsIm5iZiI6MTczMzIyNzMyOS4yNzYsInN1YiI6IjY3NGVmMzQxOTAyOWExZmNjMzZhYTY3ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.63qr-srVzSjCWOUpdktfYuBm-Wq29onvJ7dURjDElpU"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        return data["results"]
    
    else:
        return []

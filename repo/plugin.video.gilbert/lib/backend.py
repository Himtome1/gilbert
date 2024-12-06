#from path_config import configure_paths
#configure_paths()
import requests

def fetchIMDB(id):
    """
    Fetches the IMDB id of a movie based off of its TMDB id
    
    :param id: TMDB id of the movie
    :type id: str
    :return IMDB id of the movie
    :rtype str
    """
    url = "https://api.themoviedb.org/3/movie/"+id+"/external_ids"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyY2JjZTU1OTRkMGVhZGFhZGM2Zjc5MmMyZmNjMDBhNiIsIm5iZiI6MTczMzIyNzMyOS4yNzYsInN1YiI6IjY3NGVmMzQxOTAyOWExZmNjMzZhYTY3ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.63qr-srVzSjCWOUpdktfYuBm-Wq29onvJ7dURjDElpU"
    }
    print("YIUOPJASLDJAS:DJ:LAKSJ: HAHAHAH")
    response = requests.get(url, headers=headers).json()
    return(response['imdb_id'])
   
def addToRadarr(tmdb_id:str):
    """
    
    Calls Radarr API and adds movie to library

    :param imdb_id IMDB id of the movie
    :return not sure yet
    """
    url = "https://radarr.inter-datum.com/api/v3/movie"
    API_KEY = "860c7def1e4b424eb20a5df3f936b001"
    bodyJson = {
        "qualityProfileId": 6,
        "monitored": True,
        "minimumAvailability": "announced",
        "isAvailable": True,
        "tmdbId": tmdb_id,
        "id": 0,
        "addOptions": {
        "monitor": "movieOnly",
        "searchForMovie": True
        },
        "rootFolderPath": "/movies"
        }
    
    headers = {
        "accept": "application/json",
        "X-Api-Key": API_KEY
        }
    res = requests.post(url=url, headers=headers,json=bodyJson)
    resJson = res.json()
    print(resJson)
    return str(res)


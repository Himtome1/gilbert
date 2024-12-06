from path_config import configure_paths
configure_paths()
import requests
import json

# Define the API endpoint and headers
url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyY2JjZTU1OTRkMGVhZGFhZGM2Zjc5MmMyZmNjMDBhNiIsIm5iZiI6MTczMzIyNzMyOS4yNzYsInN1YiI6IjY3NGVmMzQxOTAyOWExZmNjMzZhYTY3ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.63qr-srVzSjCWOUpdktfYuBm-Wq29onvJ7dURjDElpU"
}

# Make the API request
response = requests.get(url, headers=headers)

# Ensure the response was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Save the JSON response to a file
    with open("movies.json", "w") as file:
        json.dump(data, file, indent=4)  # Use indent for pretty formatting
    
    print("Data successfully saved to movies.json")
else:
    print(f"Failed to fetch data: {response.status_code}")
    print(response.text)

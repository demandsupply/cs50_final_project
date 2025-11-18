import requests, json
from config import AUTH_CODE


headers = {
    "accept": "application/json",
    "Authorization": AUTH_CODE}

def tmdb_get(endpoint):
    url = f"https://api.themoviedb.org/3/{endpoint}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    return response.json()

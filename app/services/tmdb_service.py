import requests
from typing import Dict, List, Optional
from app.config import settings

class TMDBService:
    def __init__(self):
        self.api_key = settings.tmdb_api_key
        self.base_url = settings.tmdb_base_url
        self.genres_map = {
            28: "Action",
            12: "Adventure",
            16: "Animation",
            35: "Comedy",
            80: "Crime",
            99: "Documentary",
            18: "Drama",
            10751: "Family",
            14: "Fantasy",
            36: "History",
            27: "Horror",
            10402: "Music",
            9648: "Mystery",
            10749: "Romance",
            878: "Science Fiction",
            10770: "TV Movie",
            53: "Thriller",
            10752: "War",
            37: "Western"
        }
        
    async def get_movie_details(self, tmdb_id: int) -> Dict:
        url = f"{self.base_url}/movie/{tmdb_id}"
        params = {
            "api_key": self.api_key,
            "language": "es-ES",
            "append_to_response": "credits"
        }
        response = requests.get(url, params=params)
        return response.json()
    
    async def search_movies(self, query: str) -> List[Dict]:
        url = f"{self.base_url}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": query,
            "language": "es-ES"
        }
        response = requests.get(url, params=params)
        return response.json()["results"]

    async def get_movie_credits(self, tmdb_id: int) -> Dict:
        url = f"{self.base_url}/movie/{tmdb_id}/credits"
        params = {
            "api_key": self.api_key,
            "language": "es-ES"
        }
        response = requests.get(url, params=params)
        return response.json()

    async def get_movie_recommendations(self, tmdb_id: int) -> List[Dict]:
        url = f"{self.base_url}/movie/{tmdb_id}/recommendations"
        params = {
            "api_key": self.api_key,
            "language": "es-ES"
        }
        response = requests.get(url, params=params)
        return response.json()["results"]

    async def discover_movies_by_actor(self, actor_id: int) -> List[Dict]:
        url = f"{self.base_url}/discover/movie"
        params = {
            "api_key": self.api_key,
            "language": "es-ES",
            "with_cast": str(actor_id),
            "sort_by": "popularity.desc"
        }
        response = requests.get(url, params=params)
        return response.json()["results"]

    async def discover_movies_by_genre(self, genre_id: int) -> List[Dict]:
        url = f"{self.base_url}/discover/movie"
        params = {
            "api_key": self.api_key,
            "language": "es-ES",
            "with_genres": str(genre_id),
            "sort_by": "popularity.desc"
        }
        response = requests.get(url, params=params)
        return response.json()["results"] 
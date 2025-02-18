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
        
    async def get_movie_details(self, movie_id: int) -> Dict:
        """Get detailed information about a specific movie"""
        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            "api_key": self.api_key,
            "language": "es-ES",
            "append_to_response": "credits"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Esto lanzará una excepción si hay error
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching movie details from TMDB: {str(e)}")
            return None
    
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

    async def discover_movies_by_genre(self, genre_id: int, page: int = 1) -> List[Dict]:
        """Get movies by genre with pagination"""
        url = f"{self.base_url}/discover/movie"
        params = {
            "api_key": self.api_key,
            "language": "es-ES",
            "with_genres": str(genre_id),
            "sort_by": "popularity.desc",
            "page": page,
            "vote_count.gte": 100  # Para asegurar películas con suficientes votos
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return {
                "results": data["results"],
                "total_pages": data["total_pages"],
                "total_results": data["total_results"]
            }
        except requests.RequestException as e:
            print(f"Error fetching movies by genre: {str(e)}")
            return {"results": [], "total_pages": 0, "total_results": 0}

    async def get_movie_videos(self, movie_id: int) -> Dict:
        """Get videos (trailers, teasers) for a movie"""
        url = f"{self.base_url}/movie/{movie_id}/videos"
        params = {
            "api_key": self.api_key,
            "language": "es-ES"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Intentar obtener trailer en español primero
            videos = data.get("results", [])
            trailer = next(
                (v for v in videos if v["type"] == "Trailer" and v["site"] == "YouTube"),
                None
            )
            
            # Si no hay trailer en español, buscar en inglés
            if not trailer:
                params["language"] = "en-US"
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                videos = data.get("results", [])
                trailer = next(
                    (v for v in videos if v["type"] == "Trailer" and v["site"] == "YouTube"),
                    None
                )
            
            return trailer if trailer else None
        except Exception as e:
            print(f"Error fetching movie videos: {str(e)}")
            return None 
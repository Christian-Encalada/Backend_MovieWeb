# Inicializador de servicios

from .movie import Movie
from .actor import Actor
from .movie_actors import MovieActor
from .user import User
from .rating import Rating
from .tag import Tag
from .user_preferred_genres import UserPreferredGenres

__all__ = [
    "Movie",
    "Actor",
    "MovieActor",
    "User",
    "Rating",
    "Tag",
    "UserPreferredGenres"
]

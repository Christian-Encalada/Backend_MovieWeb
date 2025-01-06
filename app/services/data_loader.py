import pandas as pd
from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.models.link import Link

def load_movies_data(db: Session):
    movies = pd.read_csv('datasets/ml-32m/movies.csv')
    for _, row in movies.iterrows():
        movie = Movie(movie_id=row['movieId'], title=row['title'], genres=row['genres'])
        db.add(movie)
    db.commit()

def load_links_data(db: Session):
    links = pd.read_csv('datasets/ml-32m/links.csv')
    for _, row in links.iterrows():
        link = Link(movie_id=row['movieId'], imdb_id=row['imdbId'], tmdb_id=row['tmdbId'])
        db.add(link)
    db.commit()
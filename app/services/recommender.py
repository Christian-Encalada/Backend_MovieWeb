from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from .data_loader import load_movie_data

class RecommenderService:
    def __init__(self):
        self.movies, self.ratings = load_movie_data()
        self.movie_matrix = self.ratings.pivot_table(index='userId', columns='movieId', values='rating')

    def get_recommendations(self, movie_id):
        movie_ratings = self.movie_matrix[movie_id]
        similar_movies = self.movie_matrix.corrwith(movie_ratings)
        recommendations = similar_movies.sort_values(ascending=False).head(10).index.tolist()
        return recommendations
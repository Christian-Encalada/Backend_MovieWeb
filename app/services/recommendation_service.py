import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationService:
    def __init__(self):
        self.movies = pd.read_csv('datasets/ml-32m/movies.csv')
        self.movie_features = self._create_movie_features()

    def _create_movie_features(self):
        genres = self.movies['genres'].str.get_dummies('|')
        return genres

    def get_recommendations(self, movie_id: int):
        if movie_id not in self.movies['movieId'].values:
            raise KeyError("Movie not found")

        movie_idx = self.movies.index[self.movies['movieId'] == movie_id].tolist()[0]
        similarities = cosine_similarity(self.movie_features)
        similarity_scores = list(enumerate(similarities[movie_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        recommended_movie_ids = [self.movies.iloc[i[0]]['movieId'] for i in similarity_scores[1:11]]
        return recommended_movie_ids
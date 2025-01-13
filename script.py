import pandas as pd

def split_and_save_movies():
    movies = pd.read_csv('datasets/ml-32m/movies.csv')
    half = len(movies) // 8
    movies_part1 = movies.iloc[:half]
    movies_part1.to_csv('datasets/ml-32m/movies_nerff.csv', index=False)

def split_and_save_ratings():
    ratings = pd.read_csv('datasets/ml-32m/ratings.csv')
    half = len(ratings) // 8
    ratings_part1 = ratings.iloc[:half]
    ratings_part1.to_csv('datasets/ml-32m/ratings_nerff.csv', index=False)


def split_and_save_tags():
    tags = pd.read_csv('datasets/ml-32m/tags.csv')
    unique_movies = tags['movieId'].unique()
    half = len(unique_movies) // 8
    movies_part1 = unique_movies[:half]
    tags_part1 = tags[tags['movieId'].isin(movies_part1)]
    tags_part1.to_csv('datasets/ml-32m/tags_nerff.csv', index=False)

split_and_save_movies()
split_and_save_ratings()
split_and_save_tags()
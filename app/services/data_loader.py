import pandas as pd
import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_database_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT'),
            sslmode='require'
        )
        return connection
    except Error as e:
        print(f"Error conectando a PostgreSQL: {e}")
        return None

def get_valid_movie_ids(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT movie_id FROM movies")
        valid_ids = set(row[0] for row in cursor.fetchall())
        cursor.close()
        return valid_ids
    except Error as e:
        print(f"Error obteniendo IDs válidos: {e}")
        return set()

def load_ratings_data(connection, valid_movie_ids):
    try:
        cursor = connection.cursor()
        # Leer los ratings en chunks para manejar mejor la memoria
        chunk_size = 100000
        for chunk in pd.read_csv('datasets/ml-32m/ratings.csv', 
                               usecols=['movieId', 'rating'],
                               chunksize=chunk_size):
            
            # Filtrar solo los ratings de películas que existen
            valid_ratings = chunk[chunk['movieId'].isin(valid_movie_ids)]
            
            if len(valid_ratings) > 0:
                values = [(row['movieId'], row['rating']) 
                         for _, row in valid_ratings.iterrows()]
                
                cursor.executemany("""
                    INSERT INTO ratings (movie_id, rating)
                    VALUES (%s, %s)
                """, values)
                
                connection.commit()
                print(f"Procesados {len(values)} ratings válidos")
            
    except Error as e:
        print(f"Error cargando ratings: {e}")
    finally:
        cursor.close()

def load_tags_data(connection, valid_movie_ids):
    try:
        cursor = connection.cursor()
        # Leer los tags en chunks para manejar mejor la memoria
        chunk_size = 50000
        for chunk in pd.read_csv('datasets/ml-32m/tags.csv', 
                               usecols=['movieId', 'tag'],
                               chunksize=chunk_size):
            
            # Filtrar solo los tags de películas que existen
            valid_tags = chunk[chunk['movieId'].isin(valid_movie_ids)]
            
            if len(valid_tags) > 0:
                values = [(row['movieId'], row['tag']) 
                         for _, row in valid_tags.iterrows()]
                
                cursor.executemany("""
                    INSERT INTO tags (movie_id, tag)
                    VALUES (%s, %s)
                """, values)
                
                connection.commit()
                print(f"Procesados {len(values)} tags válidos")
            
    except Error as e:
        print(f"Error cargando tags: {e}")
    finally:
        cursor.close()

def main():
    connection = get_database_connection()
    if connection is not None:
        try:
            # Obtener IDs válidos de películas
            valid_movie_ids = get_valid_movie_ids(connection)
            print(f"Encontradas {len(valid_movie_ids)} películas válidas")
            
            print("Cargando ratings...")
            load_ratings_data(connection, valid_movie_ids)
            print("Cargando tags...")
            load_tags_data(connection, valid_movie_ids)
        finally:
            connection.close()
            print("Proceso de carga completado")

if __name__ == "__main__":
    main()
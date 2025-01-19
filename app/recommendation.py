import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Load dataset
songs = pd.read_csv('data/ex.csv')

# Add a unique ID for songs
songs['Song-ID'] = songs.index

# Preprocessing the ratings column to extract the numeric value
songs['User-Rating'] = songs['User-Rating'].str.extract(r'(\d+\.\d+)').astype(float)

# Create user-item matrix
song_ratings_pivot = songs.pivot(index='Song-ID', columns='Song-Name', values='User-Rating').fillna(0)

# Train collaborative filtering model
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(song_ratings_pivot.values)

def get_song_recommendations(song_name, n_recommendations=5):
    # Check if the song exists in the dataset
    if song_name not in song_ratings_pivot.columns:
        return pd.DataFrame({'error': [f"No song named '{song_name}' found in the dataset"]})
    
    # Find the index of the given song
    song_idx = song_ratings_pivot.columns.get_loc(song_name)
    
    # Get similarity scores
    distances, indices = model.kneighbors(
        [song_ratings_pivot.iloc[:, song_idx].values], n_neighbors=n_recommendations
    )
    
    # Get recommended song IDs
    recommended_song_ids = song_ratings_pivot.columns[indices.flatten()]
    return songs[songs['Song-Name'].isin(recommended_song_ids)]

def get_user_recommendations(user_rating, n_recommendations=5):
    # Filter songs with similar ratings
    user_ratings = song_ratings_pivot.mean(axis=1).values.reshape(1, -1)
    distances, indices = model.kneighbors(user_ratings, n_neighbors=n_recommendations)
    
    # Get recommended song IDs
    recommended_song_ids = song_ratings_pivot.columns[indices.flatten()]
    return songs[songs['Song-Name'].isin(recommended_song_ids)]

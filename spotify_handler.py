

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import os

# Initialize Spotify client with environment variables or replace with your credentials directly

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))


def get_mood_tracks(sp, mood, limit=10):
    # Define a list of keywords per mood to add variety
    mood_keywords = {
        'happy': ['happy', 'joyful', 'cheerful', 'good vibes'],
        'sad': ['sad', 'melancholy', 'depressed', 'heartbroken'],
        'angry': ['angry', 'rage', 'furious', 'aggressive'],
        'fear': ['fear', 'intense', 'haunting', 'dark'],
        'surprise': ['surprising', 'unexpected', 'mysterious'],
        'neutral': ['neutral', 'chill', 'lofi', 'ambient'],
        'excited': ['excited', 'party', 'energetic', 'hype'],
        'calm': ['calm', 'soothing', 'relaxing', 'meditative'],
        'romantic': ['romantic', 'love', 'valentine', 'crush'],
        'lonely': ['lonely', 'alone', 'solitude', 'isolation']
    }

    # Choose a random keyword for the selected mood
    keyword = random.choice(mood_keywords.get(mood, ['mood']))

    # Random offset to get different results every time (Spotify allows up to 1000, safe to use <100)
    offset = random.randint(0, 50)

    try:
        results = sp.search(q=keyword, type='track', limit=limit, offset=offset)
        tracks = results['tracks']['items']
        return tracks
    except Exception as e:
        print(f"Error fetching Spotify tracks: {e}")
        return []

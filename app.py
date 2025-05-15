import streamlit as st
import random
from mood_analysis import analyze_mood
from spotify_handler import get_spotify_client, get_mood_tracks
import pandas as pd

st.set_page_config(page_title="Mood vs Music", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-title {
            font-size: 3rem;
            font-weight: 800;
            color: #1DB954;
            text-align: center;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .description {
            font-size: 1.1rem;
            text-align: center;
            color: #b3b3b3;
            margin-bottom: 40px;
        }
        .track-card {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .track-card:hover {
            transform: scale(1.02);
            box-shadow: 0 0 15px #1DB954;
        }
        .track-name {
            font-size: 20px;
            font-weight: bold;
            color: #fff;
            margin-bottom: 5px;
        }
        .artist-name, .album-name {
            color: #ccc;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .track-iframe {
            border-radius: 12px;
            margin-top: 10px;
        }
        .input-area {
            width: 100%;
            height: 150px;
            padding: 12px;
            border-radius: 10px;
            border: 2px solid #1DB954;
            background-color: #2b2b2b;
            color: #fff;
            font-size: 16px;
            margin-bottom: 30px;
        }
        .loading-spinner {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .mood-icon {
            font-size: 3rem;
        }
        .mood-header {
            color: #1DB954;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎵 Mood vs Music 🎧</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Analyze your mood from text and get personalized music recommendations powered by Spotify!</div>', unsafe_allow_html=True)

user_input = st.text_area("💬 How are you feeling today?", height=150, placeholder="Type anything... I’m feeling happy and excited today!")

# Spinner for loading state
spinner = st.empty()

if st.button("Generate Playlist 🎶"):
    if not user_input.strip():
        st.warning("Please enter something to analyze your mood.")
    else:
        with spinner:
            st.spinner('Analyzing mood...')

        # Mood Analysis
        mood = analyze_mood(user_input)

        # Mood Emojis
        mood_emojis = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😡',
            'fear': '😨',
            'surprise': '😲',
            'neutral': '😐',
            'excited': '🤩',
            'calm': '😌',
            'romantic': '❤️',
            'lonely': '🥺'
        }

        emoji = mood_emojis.get(mood, '😐')
        st.markdown(f"""
            <h3 class='mood-header'>
                Detected Mood: <span style="color:#1DB954;">{mood.capitalize()}</span> {emoji}
            </h3>
        """, unsafe_allow_html=True)

        st.subheader("🎧 Your Spotify Recommendations")

        # Spotify client + get tracks
        sp = get_spotify_client()
        tracks = get_mood_tracks(sp, mood)
        random.shuffle(tracks)

        # Display each track
        for track in tracks:
            track_name = track['name']
            artist = track['artists'][0]['name']
            album = track['album']['name']
            album_cover = track['album']['images'][0]['url']
            track_url = track['external_urls']['spotify']
            track_id = track_url.split("/")[-1]

            st.markdown(f"""
                <div class="track-card">
                    <div class="track-name">{track_name}</div>
                    <div class="artist-name">{artist}</div>
                    <div class="album-name">Album: {album}</div>
                    <img src="{album_cover}" width="100px" height="100px"/>
                    <iframe class="track-iframe" 
                            src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator" 
                            width="100%" 
                            height="80" 
                            frameBorder="0" 
                            allowfullscreen="" 
                            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                            loading="lazy">
                    </iframe>
                </div>
            """, unsafe_allow_html=True)

        # ✅ ADD THIS BLOCK HERE, AFTER `tracks` IS DEFINED
        import pandas as pd
        track_data = [{
            "Track Name": t['name'],
            "Artist": t['artists'][0]['name'],
            "Album": t['album']['name'],
            "Spotify URL": t['external_urls']['spotify']
        } for t in tracks]

        df = pd.DataFrame(track_data)

        st.download_button(
            label="📥 Download Playlist as CSV",
            data=df.to_csv(index=False),
            file_name=f"{mood}_playlist.csv",
            mime="text/csv"
        )

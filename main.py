import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import streamlit as st


# Load environment variables
load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = "http://127.0.0.1:8888/callback"
scope = "user-library-read user-top-read playlist-read-private playlist-modify-private"


# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
))

# Example: get all saved tracks
def get_saved_tracks():
    results = sp.current_user_saved_tracks(limit=50)
    tracks = []
    while results:
        for item in results['items']:
            track = item['track']
            tracks.append(f"{track['name']} by {track['artists'][0]['name']}")
        if results['next']:
            results = sp.next(results)
        else:
            break
    for idx, name in enumerate(tracks):
        print(f"{idx+1}. {name}")

if __name__ == "__main__":
    get_saved_tracks()

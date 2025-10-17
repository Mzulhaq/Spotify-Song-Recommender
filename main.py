
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = "http://127.0.0.1:8888/callback"
scope = "user-library-read user-top-read playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
))

def get_liked_songs_df():
    """Return DataFrame of user's liked songs with only relevant info."""
    results = sp.current_user_saved_tracks(limit=50)
    tracks = []
    while results:
        for item in results['items']:
            track = item['track']
            tracks.append({
                'added_at': item.get('added_at'),
                'track_id': track.get('id'),
                'track_name': track.get('name'),
                'artist_name': track['artists'][0]['name'] if track.get('artists') else None,
                'album_name': track['album']['name'] if track.get('album') else None,
                'popularity': track.get('popularity'),
                'explicit': track.get('explicit'),
                'duration_ms': track.get('duration_ms'),
                'spotify_url': track['external_urls']['spotify'] if track.get('external_urls') else None
            })
        if results['next']:
            results = sp.next(results)
        else:
            break
    return pd.DataFrame(tracks)

def get_playlists_df():
    """Return DataFrame of user's playlists with only relevant info."""
    playlists = sp.current_user_playlists(limit=50)
    playlist_data = []
    for playlist in playlists['items']:
        playlist_data.append({
            'playlist_id': playlist.get('id'),
            'playlist_name': playlist.get('name'),
            'owner': playlist['owner']['display_name'] if playlist.get('owner') else None,
            'total_tracks': playlist.get('tracks', {}).get('total'),
            'spotify_url': playlist['external_urls']['spotify'] if playlist.get('external_urls') else None
        })
    return pd.DataFrame(playlist_data)

#spotify recommendations based on seed tracks, artists, and genres
#spotify recommendations endpoint is broken, function retained for future use
def get_reccommendations(seed_tracks, seed_artists=None, seed_genres=None, limit=20):
    """Get song recommendations based on seed tracks, artists, and genres."""
    recommendations = sp.recommendations(seed_tracks=seed_tracks, seed_artists=seed_artists, seed_genres=seed_genres, limit=limit)
    recs = []
    for track in recommendations['tracks']:
        recs.append({
            'track_id': track.get('id'),
            'track_name': track.get('name'),
            'artist_name': track['artists'][0]['name'] if track.get('artists') else None,
            'album_name': track['album']['name'] if track.get('album') else None,
            'popularity': track.get('popularity'),
            'explicit': track.get('explicit'),
            'duration_ms': track.get('duration_ms'),
            'spotify_url': track['external_urls']['spotify'] if track.get('external_urls') else None
        })
    return pd.DataFrame(recs)

def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id, limit=100)
    tracks = results["items"]

    # Keep fetching if there are more (pagination)
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    tracks_clean = []
    for item in tracks:
        track = item['track']
        tracks_clean.append({
            'track_id': track.get('id'),
            'track_name': track.get('name'),
            'artist_name': track['artists'][0]['name'] if track.get('artists') else None,
            'album_name': track['album']['name'] if track.get('album') else None,
            'popularity': track.get('popularity'),
            'explicit': track.get('explicit'),
            'duration_ms': track.get('duration_ms'),
            'spotify_url': track['external_urls']['spotify'] if track.get('external_urls') else None
        })

    return tracks_clean
def get_top_tracks_df():
    """Return DataFrame of user's top tracks (listening history) with only relevant info."""
    top_tracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')
    history = []
    for item in top_tracks['items']:
        history.append({
            'track_id': item.get('id'),
            'track_name': item.get('name'),
            'artist_name': item['artists'][0]['name'] if item.get('artists') else None,
            'album_name': item['album']['name'] if item.get('album') else None,
            'popularity': item.get('popularity'),
            'explicit': item.get('explicit'),
            'duration_ms': item.get('duration_ms'),
            'spotify_url': item['external_urls']['spotify'] if item.get('external_urls') else None
        })
    return pd.DataFrame(history)

if __name__ == "__main__":
    liked_songs_df = get_liked_songs_df()
    playlists_df = get_playlists_df()
    top_tracks_df = get_top_tracks_df()

    liked_songs_df.to_csv('liked_songs.csv', index=False)
    playlists_df.to_csv('playlists.csv', index=False)
    top_tracks_df.to_csv('top_tracks.csv', index=False)
    


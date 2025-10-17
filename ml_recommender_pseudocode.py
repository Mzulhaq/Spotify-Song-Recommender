import main

def get_user_song_ids():
    """
    Prompt user for song source and return a list of track IDs from liked songs, top tracks, or playlists.
    """
    choice = input("Choose song source: [liked] Liked Songs, [top] Top Tracks, [playlists] Your Playlists: ").strip().lower()
    if choice == 'liked':
        liked_songs_df = main.get_liked_songs_df()
        return liked_songs_df['track_id'].dropna().tolist()
    elif choice == 'top':
        top_tracks_df = main.get_top_tracks_df()
        return top_tracks_df['track_id'].dropna().tolist()
    elif choice == 'playlists':
        return get_playlist_song_ids_from_user()
    else:
        print("Invalid input. Please enter 'liked', 'top', or 'playlists'.")
        return []

def get_playlist_song_ids_from_user():
    """
    Prompt user to select a playlist or all playlists, then return track IDs.
    """
    playlists_df = main.get_playlists_df()
    print("\nYour Playlists:")
    print(playlists_df[['playlist_id', 'playlist_name']])
    playlist = input("Enter a playlist ID, or type 'all' for all playlists: ").strip()
    if playlist != 'all':
        try:
            tracks = main.get_playlist_tracks(playlist)
            return [track['track_id'] for track in tracks if track.get('track_id')]
        except Exception as e:
            print(f"Error fetching playlist tracks: {e}")
            return []
    else:
        playlist_ids = playlists_df['playlist_id'].dropna().tolist()
        all_playlist_tracks = []
        for pid in playlist_ids:
            try:
                tracks = main.get_playlist_tracks(pid)
                all_playlist_tracks.extend([track['track_id'] for track in tracks if track.get('track_id')])
            except Exception as e:
                print(f"Error fetching tracks for playlist {pid}: {e}")
        return list(set(all_playlist_tracks))  # Unique track IDs



if __name__ == "__main__":
    user_song_ids = get_user_song_ids()
    print(user_song_ids)
    print(f"Found {len(user_song_ids)} unique songs from your selection.")


# 2. Fetch Audio Features for User Songs
# - Use Spotify API to get audio features for each song
# user_features_df = fetch_audio_features(user_song_ids)

# 3. Build Feature Matrix
# - DataFrame: rows = songs, columns = audio features (danceability, energy, valence, etc.)
# features = ['danceability', 'energy', 'valence', 'tempo', ...]
# user_feature_matrix = user_features_df[features]

# 4. Get Candidate Songs
# - Get a pool of songs to recommend (e.g., Spotify recommendations, playlists, charts)
# candidate_song_ids = get_candidate_song_ids()
# candidate_features_df = fetch_audio_features(candidate_song_ids)
# candidate_feature_matrix = candidate_features_df[features]

# 5. Model: Find Similar Songs
# - Use KNN or cosine similarity to compare candidate songs to user's songs
# from sklearn.neighbors import NearestNeighbors
# knn = NearestNeighbors(n_neighbors=5, metric='cosine')
# knn.fit(user_feature_matrix)
# distances, indices = knn.kneighbors(candidate_feature_matrix)

# 6. Rank and Filter Recommendations
# - Exclude songs already in user's library
# - Rank by similarity (lowest distance)
# recommended_songs = select_top_n_recommendations(candidate_song_ids, distances, indices)

# 7. Display Recommendations
# - Show recommended songs (name, artist, Spotify link)
# display_recommendations(recommended_songs)

# (Optional) 8. Feedback Loop
# - Allow user to like/dislike recommendations and retrain model

# Import required packages
import streamlit as st
import pandas as pd
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Define constants for the Spotify Developer Account
# Note: For the purpose of this project, I created a separate Spotify Developer Account.
CLIENT_ID = st.secrets["SPOTIFY_ID"]
CLIENT_SECRET = st.secrets["SPOTIFY_SECRET"]
USER_NAME = st.secrets["SPOTIFY_USER"]

# Define function to convert dataframe to a csv file
@st.cache
def convert_df(df):
  return df.to_csv().encode('utf-8')

# Define function to retrieve track IDs from playlist
def get_track_IDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

# Define function to extract track metadata and track features
def get_track_features(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

    # Metadata
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # Features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    valence = features[0]['valence']

    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, energy,
             instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence]
    return track

# Write instructions for app
st.title("Download your own Spotify data!")
st.markdown("This simple app allows you to download Spotify features of songs. In order to obtain data, you must have a **Spotify playlist**. Songs must be available on Spotify to work. Once you have obtained your own data, you can upload it in the [Spotify Features Visualizer App](https://johncarlomaula-spotify-features-visualizer-project-app-05gizn.streamlitapp.com/).")
st.markdown("#### Instructions: ")
st.markdown("1. Create a Spotify playlist of your desired tracks (**maximum 100**). If you have more than 100 songs, split them up into multiple playlists. **Tip:** Avoid having duplicate songs in your playlists.")
st.markdown("2. Copy the **playlist ID** from the playlist URL. For example, in the playlist URL `https://open.spotify.com/playlist/5fp6s3NHdwxMj3H6P9zyBF`, the ID is **5fp6s3NHdwxMj3H6P9zyBF**.")
st.markdown("3. Enter a name for the output data file and the playlist ID(s) below and click **Generate Data**.")
st.markdown("**Note:** If the resulting dataframe is empty, there might have been too many data requests from Spotify. Please try again later.")
st.markdown("---")

# Text input widget for output file name
file_name = st.text_input("1. Enter your output file name (without file extension).")

# Text input widget for playist IDs
playlist_ids = st.text_area("2. Enter playlist ID(s) separated by a comma.").split(",")

# Button to generate the data
generate_data =  st.button("Generate Data")

# Obtain data if generate button is clicked
if generate_data:

    # Proceed data retrieval process if file name and playlist IDs are valid
    if file_name and playlist_ids and ".csv" not in file_name:

        # Authenticate Spotify Developer Account
        client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Call function to retrieve Spotify IDs
        IDs = []
        for id in playlist_ids:
            IDs += get_track_IDs(USER_NAME, id)
            
        # Extract features of each song
        tracks = []
        for id in IDs:
            track = get_track_features(id)
            tracks.append(track)

        # Create a dataframe of Spotify features
        df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity',
                                    'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness',
                                    'loudness', 'speechiness', 'tempo', 'time_signature', 'valence'])

        # Replace apostrophe's for consistency
        df = df.replace("’", "'", regex = True)

        # Display resulting dataframe on app
        st.markdown("#### Data:")
        st.dataframe(df)

        # Convert dataframe to a csv file
        csv = convert_df(df)

        # Button to download generated data
        st.download_button("Press to Download", csv, file_name + ".csv", "text/csv", key='download-csv')
    
    else:

        # Write warning message if file name and playist ID is not valid
        st.warning("Please enter a valid output file name and a playlist ID.")



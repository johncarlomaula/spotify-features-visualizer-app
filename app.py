# Import required packages
import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from app_functions import *

# Define constants
FEATURE_LIST = ["length", "popularity", "acousticness", "danceability", "energy", "instrumentalness",
                "liveness", "loudness", "speechiness", "tempo", "time_signature", "valence"]
METADATA = ["name", "album", "artist", "release_date"]

# Import datasets
df_adele = pd.read_csv("data/adele.csv", index_col = 0)
df_drake = pd.read_csv("data/drake.csv", index_col = 0)
df_abba = pd.read_csv("data/abba.csv", index_col = 0)
df_girlies = pd.read_csv("data/popgirlies.csv", index_col = 0)
df_rs = pd.read_csv("data/rollingstone.csv", index_col = 0)
df_bb2021 = pd.read_csv("data/bbtop2021.csv", index_col = 0)
df_bbAll = pd.read_csv("data/top15bballtime.csv", index_col = 0)

# Define dictionaty of datasets
DATASETS = {"Adele": df_adele,
            "Drake": df_drake,
            "ABBA": df_abba,
            "Pop Girlies": df_girlies,
            "Top 10 BB 200 Year-End Albums of 2021": df_bb2021,
            "Top 15 Billboard 200 All-Time Albums": df_bbAll,
            "Top 50 Rolling Stone Albums of 2010's": df_rs}

# Write instructions for app
st.title("Spotify Features Visualizer")
st.markdown("This web app allows you to visualize your Spotify music data.")
st.markdown("#### Instructions: ")
st.markdown("1. Upload your own data or select one from the available example datasets. If you would like to obtain your own data, you can do so [here](https://johncarlomaula-spotify-features-visualizer-project-data-mve406.streamlitapp.com/).")
st.markdown("2. Select what kind of visualization you would like to use. For polar charts, the data has been scaled to values between 0 and 1.")
st.markdown("3. All plots are produced using Plotly and are interactive. You can save plots, zoom in/out, filter categories, and view them in full screen.")
st.markdown("4. You can view the code on [Github](https://github.com/johncarlomaula/spotify-features-visualizer-project) and provide feedback if you'd like!")
st.markdown("5. Enjoy! 😀🎵")

# Write definition of Spotify features
st.markdown("#### Spotify Features")
with st.expander("Expand to see the list of Spotify features."):
    st.markdown("**Length** - duration of the track in minutes")
    st.markdown("**Popularity** - measurement of a song's popularity based on number of plays and how recent those plays are")
    st.markdown("**Danceability** - describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity")
    st.markdown("**Acousticness** - a confidence measure from 0.0 to 1.0 of whether the track is acoustic")
    st.markdown("**Energy** - represents a perceptual measure of intensity and activity")
    st.markdown("**Instrumentalness** - predicts whether a track contains no vocals")
    st.markdown("**Liveness** - detects the presence of an audience in the recording")
    st.markdown("**Loudness** - overall loudness of a track in decibels (dB)")
    st.markdown("**Speechiness** - detects the presence of spoken words in a track")
    st.markdown("**Tempo** - overall estimated tempo of a track in beats per minute (BPM)")
    st.markdown("**Time Signature** - an estimated time signature; the time signature (meter) is a notational convention to specify how many beats are in each bar (or measure)")
    st.markdown("**Valence** - a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track")
st.markdown("---")

# Select data
st.sidebar.header("Data:")
st.sidebar.write("Choose one of the options below. To view example datasets, there must be no file uploaded. You can remove any uploaded data by clicking the x.")
selected_data = st.sidebar.selectbox("Option 1: Example Datasets", DATASETS.keys())
uploaded_file = st.sidebar.file_uploader("Option 2: Upload data in csv format")

# Obtain data
if uploaded_file is not None:

    # Import uploaded file
    df = pd.read_csv(uploaded_file)

    # Check for unnamed column and remove if it exists
    if "Unnamed: 0" in df.columns:
        df.drop("Unnamed: 0", axis = 1, inplace = True)

elif selected_data:

    # Access selected dataset
    df = DATASETS[selected_data]

# Remove duplicates
df.drop_duplicates(inplace = True)

# Print out dataset information
st.sidebar.markdown(" ")
st.sidebar.markdown("This dataset contains {} tracks, {} artist(s), and {} albums/singles.".format(df.shape[0], len(df['artist'].unique()), len(df['album'].unique())))
st.sidebar.markdown("---")

# Select visualizations
st.sidebar.header("Visualization Options")
chart = st.sidebar.radio("Choose a visualization", ["Polar Chart", "Box Plot", "Histogram", "Scatterplot"])

if chart == "Histogram":
    plot_histogram(df)
elif chart == "Box Plot":
    plot_boxplot(df)
elif chart == "Scatterplot":
    plot_scatter(df)
elif chart == "Polar Chart":

   # Filter features
    numerical_features = st.sidebar.multiselect("Optional: Filter by features (minimum of 3)", FEATURE_LIST)

    if len(numerical_features) >= 3:
        features = METADATA + numerical_features
        df.drop(df.columns.difference(features), axis = 1, inplace = True)
    else:
        numerical_features = FEATURE_LIST

    # Scale data
    scaler = MinMaxScaler()
    df_scaled = df[METADATA]
    df_scaled[numerical_features] = scaler.fit_transform(df[numerical_features])

    # Obtain user input of album(s)
    list_of_albums = df_scaled['album'].unique().tolist()
    albums = st.sidebar.multiselect("Select album(s)", list_of_albums)

    # Calculate mean values per album
    mean_values_df = pd.DataFrame(df_scaled.groupby(['album', 'artist']).mean()).round(3)

    if albums:

        # Plot radar chart of mean values of selected albums
        st.markdown("### Mean Features by Album")
        plot_radar_chart(mean_values_df, albums, False)

        # Obtain list of songs from selected albums
        song_list = []
        for album in albums:
            song_list = song_list + df_scaled[df_scaled['album'] == album]['name'].tolist()

        # Obtain user input of songs
        if song_list:
            songs = st.sidebar.multiselect("Select song(s)", song_list)

            # Plot radar chart of selected songs
            if songs:
                df_scaled.set_index('name', inplace = True)

                st.markdown("---")
                st.markdown("### Song")

                plot_radar_chart(df_scaled, songs, True)



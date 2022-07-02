import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Define constants
FEATURE_LIST = ["length", "popularity", "acousticness", "danceability", "energy", "instrumentalness",
                "liveness", "loudness", "speechiness", "tempo", "time_signature", "valence"]
METADATA = ["name", "album", "artist", "release_date"]


# ------------------------------ HISTOGRAM FUNCTION --------------------------------- #

def plot_histogram(df):

    # Convert length from milliseconds to minutes
    df['length'] = df['length'] / 1000 / 60

    # Obtain user input of which feature to display
    feature = st.sidebar.selectbox("Select a feature", FEATURE_LIST)

    # Obtain user input of which category to filter by
    category = st.sidebar.selectbox("Filter by category", ["none", "artist", "album", "release_date"])
    
    # Plot histogram of selected feature
    if category == "none":
        st.markdown("#### Histogram of " + feature.capitalize())
        fig = px.histogram(df, x = feature)
    else:
        st.markdown("#### Histogram of " + feature.capitalize() + " by " + category.capitalize())
        st.markdown("Click on the legend to filter by " + category + ". **Tip:** View graph on full screen if it's too small.")
        fig = px.histogram(df, x = feature, color = category, barmode = "overlay") 
    
    # Display plot in app
    st.plotly_chart(fig, use_container_width = True)

# ------------------------------ BOX PLOT FUNCTION ---------------------------------- #

def plot_boxplot(df):

    # Convert length from milliseconds to minutes
    df['length'] = df['length'] / 1000 / 60

    # Obtain user input of which feature to display
    feature = st.sidebar.selectbox("Select a feature", FEATURE_LIST)

    # Obtain user input of which category to filter by  
    category = st.sidebar.selectbox("Filter by category", ["none", "artist", "album", "release_date"])
    
    # Plot histogram of selected feature
    if category == "none":
        st.markdown("#### Box Plot of " + feature.capitalize())
        fig = px.box(df, x = feature, notched = True, hover_data = METADATA)
    else:
        st.markdown("#### Box Plot of " + feature.capitalize() + " by " + category.capitalize())
        st.markdown("Click on the legend to filter by " + category + ". **Tip:** View plot on full screen if it is too small.")
        fig = px.box(df, x = feature, notched = True, color = category, hover_data = METADATA) 
    
    # Display plot in app
    st.plotly_chart(fig, use_container_width = True)

# ------------------------------ POLAR CHART FUNCTIONS ------------------------------ #

def plot_radar_chart(df, music_data, track):

    # Initialize polar chart plot
    fig = go.Figure()

    # Plot songs
    if track:
        features = df.columns.difference(["artist", "album", "release_date"])
        for song in music_data:
            add_trace(df[features], song, features, fig, df.loc[song]['artist'])
    
    # Plot albums
    else:
        features = list(df)
        for album in music_data:
            add_trace(df, album, features, fig, df.loc[album].index.values[0])
    
    # Configure plot layout
    fig.update_layout(
        polar = dict(
            radialaxis = dict(
                visible = True,
                range = [0, 1],
            )),
        legend = dict(
            yanchor = "bottom",
            y = -0.3,
            xanchor = "left",
            x = -0.1
        ),
        showlegend = True
    )

    # Display plot in app
    st.plotly_chart(fig, use_container_width = True)

def add_trace(df, album, features, fig, artist):

    # Obtain data points to plot
    values = df.loc[album].values.flatten().tolist()
    values += values[:1]

    # Add data to polar chart
    fig.add_trace(go.Scatterpolar(
        r = values,
        theta = features,
        fill = 'toself',
        opacity = 0.8,
        name = album + " - " + artist,
    ))

# ------------------------------ SCATTERPLOT FUNCTIONS ------------------------------ #

def plot_scatter(df):

    # Convert length from milliseconds to minutes
    df['length'] = df['length'] / 1000 / 60

    # Obtain user inputs for the x and y variables to display
    x = st.sidebar.selectbox("X", FEATURE_LIST)
    y = st.sidebar.selectbox("Y", FEATURE_LIST)

    st.markdown("#### Scatterplot of {} vs. {}".format(y.capitalize(), x.capitalize()))

    # Obtain user input to show trend line or not
    trend = st.sidebar.radio("Show Trend Line", ["Yes", "No"])

    # Obtain user input of which category to filter by
    category = st.sidebar.selectbox("Optional: Filter by Category", ["None", "artist", "album", "release_date"])

    # Set available customization options depending on category
    if category == "None":
        customization_options = ["None", "Size", "Color"]
    else:
        customization_options = ["None", "Size"]

    # Obtain user input to customize points
    third_feature = st.sidebar.selectbox("Optional: Customize points", customization_options)

    # Plot scatterplot depending on user inputs
    if third_feature == "None" and category == "None":
        if trend == "Yes":
            fig = px.scatter(df, x = x, y = y, trendline = "ols", hover_data = METADATA) 
        else:
            fig = px.scatter(df, x = x, y = y, hover_data = METADATA)
    elif third_feature == "Size":
        fig = customize_size(df, x, y, category, trend)
    elif third_feature == "Color":
        fig = customize_color(df, x, y, trend)
    else:
        if trend == "Yes":
            fig = px.scatter(df, x = x, y = y, color = category, trendline = "ols", hover_data = METADATA) 
        else:
            fig = px.scatter(df, x = x, y = y, color = category, hover_data = METADATA)

    # Display plot on app
    st.plotly_chart(fig, use_container_width = True)

def customize_size(df, x, y, category, trend):

    # Obtain user input of which feature to customize points by
    z = st.sidebar.selectbox("Z", FEATURE_LIST)

    # Plot scatterplot depending on user inputs
    if category == "None":
        if trend == "Yes":
            fig = px.scatter(df, x = x, y = y, trendline = "ols", size = z, hover_data = METADATA)
        else:
            fig = px.scatter(df, x = x, y = y, size = z, hover_data = METADATA)
    else:
        if trend == "Yes":
            fig = px.scatter(df, x = x, y = y, trendline = "ols", color = category, size = z, hover_data = METADATA)
        else:
            fig = px.scatter(df, x = x, y = y, color = category, size = z, hover_data = METADATA)

    return fig

def customize_color(df, x, y, trend):

    # Obtain user input of which feature to customize points by
    z = st.sidebar.selectbox("Z", FEATURE_LIST)

    # Plot scatterplot depending on user inputs
    if trend == "Yes":
        fig = px.scatter(df, x = x, y = y, trendline = "ols", color = z, hover_data = METADATA)
    else:
        fig = px.scatter(df, x = x, y = y, color = z, hover_data = METADATA)

    return fig
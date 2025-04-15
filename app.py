import pickle
import streamlit as st
import requests
import os

# Function to download file from a direct Google Drive export link
def download_file(url, destination_path):
    folder = os.path.dirname(destination_path)
    if not os.path.exists(folder):
        os.makedirs(folder)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        st.error(f"Failed to download from: {url}")
        st.stop()

# Direct Google Drive links with export=download
similarity_url = "https://drive.google.com/u/0/uc?id=1CJTivDBrWr20D9Ddi64djYtIj-AXjIgR&export=download"
movie_list_url = "https://drive.google.com/u/0/uc?id=1B4RBzV2d64wqI-plJARQhOA0kNYY53jA&export=download"

# File paths
similarity_path = "artifacts/similarity.pkl"
movie_list_path = "artifacts/movie_list.pkl"

# Download the files
download_file(similarity_url, similarity_path)
download_file(movie_list_url, movie_list_path)

# Load pickle files
try:
    with open(movie_list_path, "rb") as f:
        movies = pickle.load(f)
    with open(similarity_path, "rb") as f:
        similarity = pickle.load(f)
except Exception as e:
    st.error("Error loading pickle files. File might be corrupted or not downloaded correctly.")
    st.exception(e)
    st.stop()

# Function to get poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=434421b8cd750513a0c947e5b09c7d67&language=en-US"
    response = requests.get(url).json()
    poster_path = response.get("poster_path")
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Image"
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

# Recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

# Streamlit App UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System using Machine Learning")

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie to get recommendations", movie_list)

if st.button("Show recommended Movies"):
    with st.spinner("Finding similar movies..."):
        names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

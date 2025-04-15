import pickle
import streamlit as st
import requests
import os

# Function to download file directly from Google Drive link
def download_file_from_url(url, destination_path):
    folder_path = os.path.dirname(destination_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        st.error(f"Failed to download file from: {url}")
        st.stop()

# URLs with export=download
similarity_url = "https://drive.google.com/u/0/uc?id=1CJTivDBrWr20D9Ddi64djYtIj-AXjIgR&export=download"
movie_list_url = "https://drive.google.com/u/0/uc?id=1B4RBzV2d64wqI-plJARQhOA0kNYY53jA&export=download"

# Local paths
similarity_file_path = 'artifacts/similarity.pkl'
movie_list_file_path = 'artifacts/movie_list.pkl'

# Download the files
download_file_from_url(similarity_url, similarity_file_path)
download_file_from_url(movie_list_url, movie_list_file_path)

# Load the pickle files safely
try:
    with open(movie_list_file_path, 'rb') as f:
        movies = pickle.load(f)
    with open(similarity_file_path, 'rb') as f:
        similarity = pickle.load(f)
except Exception as e:
    st.error("Failed to load model files. Ensure that the files are valid .pkl format.")
    st.exception(e)
    st.stop()

# Fetch poster using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=434421b8cd750513a0c947e5b09c7d67&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Image"
    return "http://image.tmdb.org/t/p/w500/" + poster_path

# Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)
    recommended_movies_names = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_names.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies_names, recommended_movies_poster

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System using Machine Learning")

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie to get recommendations", movie_list)

if st.button('Show recommended Movies'):
    with st.spinner("Finding similar movies..."):
        recommended_movies_names, recommended_movies_poster = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movies_names[i])
            st.image(recommended_movies_poster[i])

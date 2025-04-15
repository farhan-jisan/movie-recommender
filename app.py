import pickle
import streamlit as st
import requests
import gdown
import os

# Function to download a file from Google Drive with fallback
def download_from_drive(file_id, destination_path):
    folder_path = os.path.dirname(destination_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    url = f"https://drive.google.com/uc?id={file_id}"
    try:
        gdown.download(url, destination_path, quiet=False)
    except Exception as e:
        # Fallback using requests if gdown fails
        st.warning(f"gdown failed, falling back to requests: {e}")
        response = requests.get(url, stream=True)
        with open(destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

# Download similarity.pkl from Google Drive
similarity_file_id = '1CJTivDBrWr20D9Ddi64djYtIj-AXjIgR'
similarity_file_path = 'artifacts/similarity.pkl'
download_from_drive(similarity_file_id, similarity_file_path)

# Download movie_list.pkl from Google Drive
movie_list_file_id = '1B4RBzV2d64wqI-plJARQhOA0kNYY53jA'
movie_list_file_path = 'artifacts/movie_list.pkl'
download_from_drive(movie_list_file_id, movie_list_file_path)

# Load movie data and similarity matrix
movies = pickle.load(open(movie_list_file_path, 'rb'))
similarity = pickle.load(open(similarity_file_path, 'rb'))

# Function to fetch movie poster using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=434421b8cd750513a0c947e5b09c7d67&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Image"
    return "http://image.tmdb.org/t/p/w500/" + poster_path

# Recommend function
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

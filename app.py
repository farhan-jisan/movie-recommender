import pickle
import streamlit as st
import requests


# Load movie data and similarity matrix from precomputed files
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))



# Function to fetch movie poster using TMDB API
# Takes movie id and returns URL of the poster
def fetch_poster(movie_id):
    # api_key = "434421b8cd750513a0c947e5b09c7d67"
    url = "https://api.themoviedb.org/3/movie/{}?api_key=434421b8cd750513a0c947e5b09c7d67&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    # Fallback if poster is not found

    poster_path = data.get('poster_path')
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Image"

    full_path = "http://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



# Function to recommend movies
# Takes a movie title and returns 5 recommended movie titles and their posters

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]  # Find index of the input movie
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)  # Sort by similarity

    recommended_movies_names = []
    recommended_movies_poster = []

    for i in distances [1:6]: # skipping the first one as it is the selected movie itself
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_names.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies_names, recommended_movies_poster


# Streamlit UI setup

st.set_page_config(page_title = "Movie Recommender", layout = "wide")
st.title("🎬 Movie Recommendation System using Machine Learning")

# Dropdown to select movie

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie to get recommendations", movie_list)


# Show recommendations when the button is clicked

if st.button('Show recommended Movies'):
    with st.spinner("Finding similar movies..."):
        recommended_movies_names, recommended_movies_poster = recommend(selected_movie)


    # Display the result in 5 columns

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movies_names[i])
            st.image(recommended_movies_poster[i])

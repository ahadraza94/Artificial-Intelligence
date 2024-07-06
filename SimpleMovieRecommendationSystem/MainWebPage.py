import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index
    if len(movie_index) == 0:
        return [], []  # Return empty lists if movie is not found
    index = movie_index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Custom CSS
st.markdown("""
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }
        .header {
            padding: 20px;
            text-align: center;
            background-color: #007bff;
            color: #fff;
            margin-bottom: 20px;
        }
        .button {
            background-color: #007bff;
            color: #fff;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin-bottom: 20px;
            cursor: pointer;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .recommendation-section {
            margin: 20px;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .movie-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .movie-card {
            width: 200px;
            margin-bottom: 20px;
            text-align: center;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        .movie-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        .movie-title {
            font-weight: bold;
            margin-top: 10px;
        }
        .movie-poster {
            width: 150px;
            height: 220px;
            object-fit: cover;
            border-radius: 10px 10px 0 0;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header"><h1>Movie Recommender System</h1></div>', unsafe_allow_html=True)

# User input
selected_movie = st.selectbox("Select a movie:", movies['title'].values)

# Recommendation button
if st.button('Get Recommendations', key='recommendation_button'):
    st.markdown('<div class="recommendation-section">', unsafe_allow_html=True)
    st.write("<h2>Recommended Movies for You:</h2>", unsafe_allow_html=True)
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    st.markdown('<div class="movie-container">', unsafe_allow_html=True)
    for i in range(5):
        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
        st.image(recommended_movie_posters[i], caption=recommended_movie_names[i], use_column_width=True)
        st.write(f"<p class='movie-title'>{recommended_movie_names[i]}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

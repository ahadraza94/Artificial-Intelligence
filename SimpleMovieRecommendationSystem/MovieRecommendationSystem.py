import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem.porter import PorterStemmer
import pickle

# Load data
movies = pd.read_csv('MovieDataset/tmdb_5000_credits.csv')
credits = pd.read_csv('MovieDataset/tmdb_5000_movies.csv')

# Merge dataframes
movies = movies.merge(credits, on='title')

# Select relevant columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'cast', 'keywords', 'crew']]

# Drop missing values
movies.dropna(inplace=True)

# Convert stringified lists to actual lists
for column in ['genres', 'keywords', 'cast', 'crew']:
    movies[column] = movies[column].apply(lambda x: [i['name'] for i in eval(x)])

# Preprocess overview text
stemmer = PorterStemmer()
movies['overview'] = movies['overview'].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split()]))

# Create tags
movies['tags'] = movies['overview'] + ' ' + movies['genres'].apply(lambda x: ' '.join(x)) + ' ' + \
                 movies['keywords'].apply(lambda x: ' '.join(x)) + ' ' + \
                 movies['cast'].apply(lambda x: ' '.join(x)) + ' ' + \
                 movies['crew'].apply(lambda x: ' '.join(x))

# Lowercase tags
movies['tags'] = movies['tags'].apply(lambda x: x.lower())

# Vectorize tags
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# Calculate similarity matrix
similarity = cosine_similarity(vectors)

# Define recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies.iloc[i[0]]['title'] for i in movies_list]
    return recommended_movies

# Test recommendation function
recommendations = recommend('Batman Begins')
print(recommendations)

# Export data and model
pickle.dump(movies, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem.porter import PorterStemmer

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def load_and_process_data():
    try:
        movies = pd.read_csv('tmdb_5000_movies.csv.zip')
        credits = pd.read_csv('tmdb_5000_credits.csv.zip')
    except FileNotFoundError:
        # If zip files not found, try without .zip
        try:
            movies = pd.read_csv('tmdb_5000_movies.csv')
            credits = pd.read_csv('tmdb_5000_credits.csv')
        except FileNotFoundError:
            raise FileNotFoundError("Dataset files not found. Please ensure tmdb_5000_movies.csv and tmdb_5000_credits.csv are in the project directory.")

    movies = movies.merge(credits, on='title')
    movies = movies[['movie_id', 'genres', 'keywords', 'title', 'overview', 'cast', 'crew']]
    movies.dropna(inplace=True)

    def convert(obj):
        l = []
        for i in ast.literal_eval(obj):
            l.append(i['name'])
        return l

    def convert2(obj):
        l = []
        counter = 0
        for i in ast.literal_eval(obj):
            if counter != 3:
                l.append(i['name'])
                counter += 1
            else:
                break
        return l

    def fetch_director(obj):
        l = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                l.append(i['name'])
                break
        return l

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert2)
    movies['crew'] = movies['crew'].apply(fetch_director)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    # Remove spaces
    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    new_df = movies[['movie_id', 'title', 'tags']]
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
    new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

    ps = PorterStemmer()
    def stem(text):
        y = []
        for i in text.split():
            y.append(ps.stem(i))
        return " ".join(y)

    new_df["tags"] = new_df["tags"].apply(stem)

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    similarity = cosine_similarity(vectors)

    return new_df, similarity

def recommend(movie, new_df, similarity):
    try:
        movie_index = new_df[new_df["title"] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommendations = [new_df.iloc[i[0]].title for i in movies_list]
        return recommendations
    except IndexError:
        return ["Movie not found in database"]

def get_movie_list(new_df):
    return sorted(new_df['title'].tolist())
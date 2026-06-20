
import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import os
def load_pickle(url):
    response = requests.get(url)
    return pickle.loads(response.content)


def download_file(url, filename):
    # If already downloaded → skip
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")

        response = requests.get(url, stream=True)
        with open(filename, "wb") as f:
            for chunk in response.iter_content(1024):
                if chunk:
                    f.write(chunk)

        print(f"{filename} downloaded!")

    else:
        print(f"{filename} already exists. Skipping download.")

    return pickle.load(open(filename, "rb"))

movies_url = "https://www.dropbox.com/scl/fi/5q3m535h1iy2s33798qcy/movies.pkl?rlkey=6m7mw3v2f08ftmafdm8ng71qr&st=fxdvo14h&dl=1"

similarity_url = "https://www.dropbox.com/scl/fi/cr9l16g9mgfqy3amgzypj/similarity.pkl?rlkey=ezccgy3qi0ghj1poerhn0jpm5&st=gz5rs3bt&dl=1"

API_KEY = "5d3e9c7f397530f090373c398cac5f74"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #ffffff;
}

.sub-text {
    text-align: center;
    font-size: 18px;
    color: #aaaaaa;
    margin-bottom: 30px;
}

.movie-card {
    padding: 15px;
    border-radius: 15px;
    background-color: #1c1f26;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}

img {
    border-radius: 10px;
}

.movie-card:hover {
    transform: scale(1.05);
}

.stButton>button {
    width: 100%;
    height: 50px;
    font-size: 18px;
    border-radius: 12px;
    background-color: #ff4b4b;
    color: white;
    font-weight: bold;
}

div[data-baseweb="select"] {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="main-title">🎬 Movie Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Find movies you will love ❤️</div>', unsafe_allow_html=True)



# ---------------- FUNCTION ----------------

@st.cache_data
def load_data():
    with st.spinner("Downloading and loading data... ⏳ (first time only)"):
        movies = download_file(movies_url, "movies.pkl")
        similarity = download_file(similarity_url, "similarity.pkl")
    return movies, similarity
movies, similarity = load_data()

@st.cache_data
def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        response = requests.get(url)

        if response.status_code != 200:
            print("API ERROR:", response.status_code)
            return "https://via.placeholder.com/500x750?text=Error", "Error", "N/A", "N/A"

        data = response.json()

        poster = (
            "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            if data.get('poster_path')
            else "https://via.placeholder.com/500x750?text=No+Image"
        )

        overview = data.get('overview', "No overview available")
        rating = data.get('vote_average', "N/A")
        release_date = data.get('release_date', "N/A")

        return poster, overview, rating, release_date

    except Exception as e:
        print("ERROR:", e)
        return "https://via.placeholder.com/500x750?text=Error", "Error", "N/A", "N/A"

def recommend(movie, selected_genre):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])

    names, posters, overviews, ratings, dates = [], [], [], [], []

    for i in movies_list[1:]:
        movie_data = movies.iloc[i[0]]

        # 🔥 FILTER LOGIC
        if selected_genre != "All":
            if selected_genre.lower() not in movie_data['tags'].lower():
                continue

        movie_id = movie_data.movie_id

        poster, overview, rating, release_date = fetch_movie_details(movie_id)

        names.append(movie_data.title)
        posters.append(poster)
        overviews.append(overview)
        ratings.append(rating)
        dates.append(release_date)

        if len(names) == 5:
            break

    return names, posters, overviews, ratings, dates
# ---------------- LOAD DATA ----------------

all_genres = set()

# Extract genres from tags (basic keywords)
possible_genres = [
    "action", "comedy", "drama", "romance",
    "thriller", "horror", "adventure",
    "animation", "fantasy", "crime"
]

for tag_string in movies['tags']:
    tag_string = tag_string.lower()
    for g in possible_genres:
        if g in tag_string:
            all_genres.add(g.capitalize())

all_genres = sorted(list(all_genres))


# ---------------- Top Trending Movies ----------------
st.markdown("## 🔥 Trending Movies")

trending_movies = movies.iloc[0:5]
cols = st.columns(5)

for i, col in enumerate(cols):
    with col:
        movie_id = trending_movies.iloc[i]['movie_id']
        poster, overview, rating, release_date = fetch_movie_details(movie_id)

        st.image(poster)
        st.caption(trending_movies.iloc[i]['title'])
        st.write(f"⭐ {rating}")


# ---------------- SELECT BOX ----------------

selected_movie = st.selectbox("🔍 Search a movie", movies['title'].values)


# ---------------- SIDEBAR FILTER ----------------
st.sidebar.header("🎯 Filters")

selected_genre = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + all_genres
)


# ---------------- BUTTON ----------------
if st.button("🎯 Recommend"):
    with st.spinner("Finding best movies for you... 🔍"):
        names, posters, overviews, ratings, dates = recommend(selected_movie, selected_genre)

    st.markdown("---")

    # ---------------- RESULT GRID ----------------
    cols = st.columns(5, gap="large")

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)

            st.markdown(f"### 🎬 {names[i]}")
            st.markdown(f"⭐ {ratings[i]}")
            st.markdown(f"📅 {dates[i]}")

            with st.expander("📖 Overview"):
                st.write(overviews[i])




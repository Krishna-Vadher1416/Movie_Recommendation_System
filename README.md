# 🎬 Movie Recommendation System

A Machine Learning-based Movie Recommendation System that suggests movies based on user preferences using content-based filtering.

---

## 🚀 Features

* 🔍 Search for any movie
* 🎯 Get top recommended similar movies
* 🎭 Genre-based filtering
* ⭐ Movie ratings and details
* 🎨 Interactive UI using Streamlit

---

## 🧠 How It Works

This project uses **Content-Based Filtering**:

* Movie metadata (genres, keywords, cast, etc.) is combined into a single feature (`tags`)
* Text data is converted into numerical vectors using **CountVectorizer**
* Similarity between movies is calculated using **Cosine Similarity**
* Based on similarity scores, top recommended movies are displayed

---

## 🛠️ Tech Stack

* Python 🐍
* Pandas & NumPy
* Scikit-learn
* Streamlit
* TMDB API (for movie details & posters)

---

## 📂 Project Structure

```
Movie_Recommendation_System/
│── app.py
│── requirements.txt
│── README.md
│── movies.pkl (not included)
│── similarity.pkl (not included)
```

---

## ⚠️ Important Note

Due to large file size, the trained model files (`movies.pkl` and `similarity.pkl`) are **not included** in this repository.

### 👉 To run the project:

1. Download the files from:

   * Movies: https://www.dropbox.com/scl/fi/5q3m535h1iy2s33798qcy/movies.pkl?rlkey=6m7mw3v2f08ftmafdm8ng71qr&st=fxdvo14h&dl=1
   * Similarity: https://www.dropbox.com/scl/fi/cr9l16g9mgfqy3amgzypj/similarity.pkl?rlkey=ezccgy3qi0ghj1poerhn0jpm5&st=gz5rs3bt&dl=1

2. Place them in the project folder

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📸 Demo

(Add screenshots here if you want)

---

## 📌 Future Improvements

* Deploy the application (Render / Streamlit Cloud)
* Add user authentication
* Improve recommendation accuracy
* Add collaborative filtering

---

## 🙌 Acknowledgements

* TMDB API for movie data
* Scikit-learn for ML tools

---

## 📬 Contact

If you like this project or want to collaborate, feel free to connect!

---

⭐ Don't forget to star the repository if you found it useful!

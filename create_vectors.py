import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer

# Load dataset
movies = pd.read_csv('tmdb_5000_movies.csv')

# Create tags column (important)
movies['tags'] = movies['overview'].fillna('') + movies['genres'].fillna('')

# Convert to string
movies['tags'] = movies['tags'].astype(str)

# Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# Save vectors
pickle.dump(vectors, open('movies.pkl', 'wb'))

print("✅ vectors.pkl created successfully")


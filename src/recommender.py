import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load data
embeddings = np.load("./src/embeddedData/movie_embeddings.npy", allow_pickle=True)
moviesData = pd.read_csv("./src/dataset/moviesData.csv")

# Fill missing values
moviesData["keywords"] = moviesData["keywords"].fillna("")
moviesData["genres"] = moviesData["genres"].fillna("")


def compute_keyword_similarity(movie_keywords, all_keywords):
    """
    Computes Jaccard similarity between a movie's keywords and all movies in the dataset.
    """
    similarities = []
    movie_set = set(movie_keywords.split(", "))

    for keywords in all_keywords:
        if isinstance(keywords, str):  # Ensure keywords is not NaN
            other_set = set(keywords.split(", "))
            intersection = len(movie_set & other_set)
            union = len(movie_set | other_set)
            similarity = intersection / union if union > 0 else 0
        else:
            similarity = 0  # If no keywords available

        similarities.append(similarity)

    return np.array(similarities)


def compute_genre_similarity(moviesData, movie_index):
    """
    Computes genre similarity using TF-IDF + Cosine Similarity.
    """
    vectorizer = TfidfVectorizer()
    genre_matrix = vectorizer.fit_transform(moviesData["genres"])
    return cosine_similarity(genre_matrix[movie_index], genre_matrix)[0]


def recommend_movies(
    movie_title, release_year=None, top_n=9, alpha=0.7, beta=0.5, gamma=0.1
):
    """
    Recommends movies based on embeddings, keywords, genre similarity, and popularity.

    Args:
        movie_title (str): The title of the movie to base recommendations on.
        release_year (int, optional): Filter recommendations by release year.
        top_n (int, optional): Number of recommendations to return.
        alpha (float, optional): Weight for embedding similarity (default: 0.6).
        beta (float, optional): Weight for keyword similarity (default: 0.25).
        gamma (float, optional): Weight for genre similarity (default: 0.3).

    Returns:
        DataFrame: Recommended movies.
    """

    # Find the index of the selected movie
    movie_index = moviesData[
        moviesData["title"].str.lower() == movie_title.lower()
    ].index

    if len(movie_index) == 0:
        return "Movie not found!"

    movie_index = movie_index[0]

    # Compute cosine similarity using embeddings
    selected_embedding = np.array(embeddings[movie_index]).reshape(1, -1)
    embedding_similarities = cosine_similarity(selected_embedding, embeddings)[0]

    # Compute keyword similarity
    selected_keywords = moviesData["keywords"].iloc[movie_index]
    keyword_similarities = compute_keyword_similarity(
        selected_keywords, moviesData["keywords"]
    )

    # Compute genre similarity
    genre_similarities = compute_genre_similarity(moviesData, movie_index)

    # Compute combined score
    combined_scores = (
        alpha * embedding_similarities
        + beta * keyword_similarities
        + gamma * genre_similarities
    )

    # Apply release year filter if provided
    if release_year:
        recommendations_df = moviesData[
            moviesData["release_year"] == release_year
        ].copy()
    else:
        recommendations_df = moviesData.copy()

    # Compute final score (popularity weight reduced)
    recommendations_df["score"] = combined_scores[recommendations_df.index] + (
        0.05 * recommendations_df["popularity_normalized"]
    )

    # Remove the queried movie itself
    recommendations_df = recommendations_df[
        recommendations_df["title"].str.lower() != movie_title.lower()
    ]

    # Sort and return top recommendations
    recommendations = recommendations_df.nlargest(top_n, "score")[
        ["title", "score", "release_year", "genres", "overview"]
    ]

    return recommendations


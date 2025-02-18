import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv("./dataset/TMDB_movie_dataset_v11.csv")

moviesData = data[
    [
        "title",
        "status",
        "adult",
        "original_language",
        "original_title",
        "overview",
        "popularity",
        "tagline",
        "genres",
        "keywords",
        "release_date",
    ]
].copy()  


def preprocessingData(moviesData):
    # Remove duplicates
    moviesData = moviesData.drop_duplicates(subset=["title"]).copy()

    # Extract release year
    moviesData.loc[:, "release_year"] = pd.to_datetime(
        moviesData["release_date"], errors="coerce"
    ).dt.year

    # Drop NaNs in release_year and convert to int
    moviesData = moviesData.dropna(subset=["release_year"]).copy()
    moviesData.loc[:, "release_year"] = moviesData["release_year"].astype(int)

    # Filter movies released between 2010 and 2027
    moviesData = moviesData[
        (moviesData["release_year"] >= 2010) & (moviesData["release_year"] <= 2027)
    ].copy()

    moviesData["keywords"] = moviesData["keywords"].fillna("")
    moviesData["genres"] = moviesData["genres"].fillna("")

    # Filter common languages (at least 2500 occurrences)
    language_counts = moviesData["original_language"].value_counts()
    languages_to_keep = language_counts[language_counts >= 2500].index
    moviesData = moviesData[
        moviesData["original_language"].isin(languages_to_keep)
    ].copy()

    # Normalize popularity
    scaler = MinMaxScaler()
    moviesData.loc[:, "popularity_normalized"] = scaler.fit_transform(
        moviesData[["popularity"]]
    )

    # Fill missing popularity with 0
    moviesData.loc[:, "popularity"] = moviesData["popularity"].fillna(0)

    return moviesData

moviesData = preprocessingData(moviesData)

moviesData["features"] = (
    moviesData["overview"] + " " + moviesData["genres"]
)

moviesData["features"] = moviesData["features"].astype(str)
moviesData.to_csv("./dataset/moviesData.csv", index=False)

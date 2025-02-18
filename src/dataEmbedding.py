import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os
import torch


device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("all-mpnet-base-v2").to(device)

# Load movie data
moviesData = pd.read_csv("./dataset/moviesData.csv")


def encode_movie_features(movie_data, model, batch_size=32, checkpoint_interval=100):
    """
    Encodes movie features into embeddings and saves them periodically.

    Args:
        movie_data (DataFrame): A DataFrame containing movie data with a 'features' column.
        model: The model used to encode the text.
        batch_size (int): The number of samples to process in one batch.
        checkpoint_interval (int): How often (in batches) to save a checkpoint.

    Returns:
        embeddings (np.ndarray): The encoded movie embeddings.
    """
    embeddings = []
    texts = movie_data["features"].tolist()

    # Process in batches
    for i in tqdm(
        range(0, len(texts), batch_size), desc="Encoding Movies", unit="batch"
    ):
        batch = texts[i : i + batch_size]

        # Encode batch and move it to the correct device
        batch_embeddings = model.encode(
            batch, batch_size=batch_size, show_progress_bar=False, device=device
        )
        embeddings.extend(batch_embeddings)  # Append batch results to main list

    # Convert to NumPy array for saving
    embeddings = np.array(embeddings)

    output_dir = "./embeddedData"
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Save final embeddings
    np.save(os.path.join(output_dir, "movie_embeddings.npy"), embeddings)

    return embeddings


# Encode movie features
embeddings = encode_movie_features(moviesData, model)

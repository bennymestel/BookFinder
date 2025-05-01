import pandas as pd
from sentence_transformers import SentenceTransformer
from google.colab import drive
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check if drive is already mounted
if not os.path.ismount('/content/drive'):
    drive.mount('/content/drive')

# Load CSV file
excel_file = '/content/drive/My Drive/from_idea_to_app/500_bestselling_titles_with_genre.csv'
df = pd.read_csv(excel_file)
logging.info(f"Loaded CSV file: {excel_file}")

# Load pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")
logging.info("Loaded SentenceTransformer model")

# Create a column for embeddings
embeddings = []

# Iterate through the DataFrame rows
for index, row in df.iterrows():
    book_name = row['title']
    author_name = row['author']
    description = row['description']
    genre = row['genre']

    # Combine description, author_name, and genre
    combined_text = f"Genre: {genre}. Book: {description}. Genre: {genre}. Author: {author_name}."

    # Log combined text
    logging.debug(f"Combined text for '{book_name}': {combined_text}")

    # Encode the combined text
    embedding = model.encode(combined_text).tolist()

    # Append embedding to list
    embeddings.append(embedding)
    logging.info(f"Generated embedding for '{book_name}' by '{author_name}'")

# Add embeddings as a new column in the DataFrame
df['embedding'] = embeddings

# Save the DataFrame with embeddings to a CSV file in Google Drive
output_file = '/content/drive/My Drive/from_idea_to_app/book_embeddings.csv'
df.to_csv(output_file, index=False)
logging.info(f"Saved embeddings to {output_file}")

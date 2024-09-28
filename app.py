import streamlit as st
import requests
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="BookFinder", page_icon="📚")

# Mount Google Drive (for Colab, comment out if running locally)
# from google.colab import drive
# drive.mount('/content/drive')

# Load the CSV file from Google Drive
@st.cache_resource
def load_data():
    # Load CSV file from Google Drive (adjust path accordingly)
    csv_file = 'book_embeddings.csv'  # Replace with your path
    df = pd.read_csv(csv_file)
    return df

df = load_data()

# Cache the models
@st.cache_resource
def load_models():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    summarizer = pipeline("summarization", model="t5-small")
    return model, summarizer

model, summarizer = load_models()

# Function to search books using Google Books API
def search_books(query, author, api_key):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{query}+inauthor:{author}&langRestrict=en&key={api_key}"
    st.write("This is the api call "+url)
    response = requests.get(url)

    # Print the response status code for debugging
    st.write(f"Full response: {response}")
    st.write(f"API Status Code: {response.status_code}")
    
    if response.status_code == 200:
        books = response.json()
        return books
    else:
        # Print the error response for further investigation
        st.write(f"Error: {response.text}")
        return None

# Function to get the first description from the search results
def get_first_description(books):
    if 'items' in books:
        for item in books['items']:
            if 'description' in item['volumeInfo'] and item['volumeInfo']['language'] == 'en':
                return item['volumeInfo']['description'], item['volumeInfo']['authors'], item['volumeInfo']['categories']
    return None

# Function to summarize text
def summarize_text(text, max_length=100):
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Function to find similar books using the CSV data
def find_similar_books(input_description):
    # Embed the input description
    input_embedding = model.encode(input_description).reshape(1, -1).astype(np.float32)
    
    # Retrieve embeddings and metadata from the DataFrame
    embeddings = df['embedding'].apply(lambda x: np.fromstring(x[1:-1], sep=',').astype(np.float32)).values
    descriptions = df[['title', 'author', 'description']].values
    
    # Compute cosine similarities
    embeddings = np.vstack(embeddings)
    similarities = util.cos_sim(input_embedding, embeddings)[0]
    
    # Sort by similarity
    sorted_indices = np.argsort(-similarities)
    
    # Prepare results
    results = []
    for idx in sorted_indices[:5]:
        book_name, author_name, text = descriptions[idx]
        results.append({
            "Book Name": book_name,
            "Author": author_name,
            "Description": text,
            "Similarity": f"{similarities[idx].item():.4f}"
        })
    
    return results

# Streamlit UI
st.title("Book Finder")

book_title = st.text_input("Enter the title of a book you like:")
book_author = st.text_input("Enter the author:")
api_key = st.secrets["google_books_api_key"]["key"]  # Use Streamlit's secrets management

if st.button("Find Similar Books"):
    if book_title and book_author:
        with st.spinner("Searching for books..."):
            books = search_books(book_title, book_author, api_key)
            if books:
                description, author, genre = get_first_description(books)
                if description:
                    summarized_description = summarize_text(description)
                    if author and genre:
                        summarized_description += " " + author[0] + "-" + genre[0]
                    st.write(f"Summarized description: {summarized_description}")
                    similar_books = find_similar_books(summarized_description)
                    st.write("Top 5 similar books:")
                    st.dataframe(similar_books)
                else:
                    st.write("No description found")
            else:
                st.write("Failed to retrieve books")
    else:
        st.write("Please provide both the book title and author")

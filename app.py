import streamlit as st
import streamlit.components.v1 as components
import requests
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import streamlit_analytics

# Set page configuration
st.set_page_config(page_title="BookFinder", page_icon="📚")

with streamlit_analytics.track():
    st.text_input("Write something")
    st.button("Click me")

# Load the CSV file
@st.cache_resource
def load_data():
    csv_file = 'book_embeddings_with_links.csv'  # Replace with your path
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
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{query}+inauthor:{author}&langRestrict=en&key={api_key}&country=US"
    response = requests.get(url)

    # Print the response status code for debugging
    st.write(f"API Status Code: {response.status_code}")
    
    if response.status_code == 200:
        books = response.json()
        return books
    else:
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
    descriptions = df[['title', 'author', 'description', 'Libgen_Link_1', 'Libgen_Link_2']].values  # Added link columns
    
    # Compute cosine similarities
    embeddings = np.vstack(embeddings)
    similarities = util.cos_sim(input_embedding, embeddings)[0]
    
    # Sort by similarity
    sorted_indices = np.argsort(-similarities)
    
    # Prepare results
    results = []
    for idx in sorted_indices[:5]:
        book_name, author_name, text, link1, link2 = descriptions[idx]
        results.append({
            "Book Name": book_name,
            "Author": author_name,
            "Description": text,
            "Download link 1": link1 if link1 else 'N/A',
            "Download link 2": link2 if link2 else 'N/A'
        })
    
    return pd.DataFrame(results)

# Function to make clickable links in the DataFrame
def make_clickable(val):
    """Convert URL into clickable link"""
    if isinstance(val, str) and val.startswith('http'):
        return f'<a href="{val}" target="_blank">Download</a>'
    return 'N/A'  # Return 'N/A' if the value is not a valid link


# Streamlit UI
st.title("Book Finder")

book_title = st.text_input("Enter the title of a book you like:")
book_author = st.text_input("Enter the author:")
api_key = st.secrets["google_books_api_key"]["key"]

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
                    
                    # Find similar books
                    similar_books = find_similar_books(summarized_description)
                    
                    # Apply the clickable link formatting to Download link 1 and Download link 2
                    similar_books['Download link 1'] = similar_books['Download link 1'].apply(make_clickable)
                    similar_books['Download link 2'] = similar_books['Download link 2'].apply(make_clickable)

                    similar_books.index = np.arange(1, len(similar_books) + 1)
                    
                    # Render the DataFrame with links (allow HTML rendering)
                    st.write(similar_books.to_html(escape=False), unsafe_allow_html=True)
                else:
                    st.write("No description found")
            else:
                st.write("Failed to retrieve books")
    else:
        st.write("Please provide both the book title and author")

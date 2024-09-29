# BookFinder - Final Project

**BookFinder** is a web application that allows users to find books similar to ones they've enjoyed by analyzing book descriptions and genres. It leverages the power of natural language processing to compare book descriptions and retrieve recommendations from a custom dataset.

## Features

- **Search for books** using the Google Books API by providing a book title and author.
- **Summarizes** the description of the book and uses it to find similar books from a pre-loaded dataset.
- Displays results with **clickable download links** (Libgen) for easy access to the recommended books.

## Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Frontend framework used to build the interactive web application.
- **Transformers**: Used for text summarization (`t5-small` model).
- **Sentence-Transformers**: Used for sentence embeddings to find similar books.
- **Pandas**: Data manipulation and analysis.
- **NumPy**: Used for numerical operations.
- **Google Books API**: Used to retrieve book data by title and author.

## Files in the Repository

- **app.py**: Main file that runs the Streamlit web app and includes all the logic for searching books, summarizing descriptions, and recommending similar books.
- **book_embeddings_with_links.csv**: A CSV file containing book metadata and embeddings used for finding similar books.
- **requirements.txt**: A list of all the dependencies required to run the project.
- **generate_embeddings.py**: Script used to generate the book embeddings from the raw data.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/bennymestel/BookFinder_FinalProject.git
   cd BookFinder_FinalProject```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your Google Books API key to the streamlit secrets file:

   ```bash
   [google_books_api_key]
   key = "YOUR_GOOGLE_BOOKS_API_KEY"
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```
   
5. Open the browser to view the app at http://localhost:8501.

## How to Generate Book Embeddings
The book_embeddings_with_links.csv file contains metadata about books (title, author, description, and download links) along with precomputed embeddings for each book description. These embeddings were generated using the SentenceTransformer model (all-MiniLM-L6-v2).

If you want to generate or update the book embeddings, you can use the script generate_embeddings.py provided in this repository. The script processes a CSV file containing book metadata (title, author, description, and genre), creates embeddings using the Sentence-Transformers library, and saves the updated data with embeddings in a new CSV file.

**Steps**:
1. Install the required dependencies by following the instructions in requirements.txt.

2. Run the embedding script:

Ensure you have a CSV file containing book metadata.
Modify the file paths in the generate_embeddings.py script as needed.
Run the script:

   ```bash
   python generate_embeddings.py
```
The embeddings will be saved to a new CSV file, which can then be used in the main application.

## Author
Benny Mestel

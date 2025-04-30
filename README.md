# BookFinder - Final Project

**BookFinder** is a web application that helps users discover books similar to their favorites by analyzing book descriptions and genres. It leverages natural language processing to compare book descriptions and provide personalized recommendations from a custom dataset.

## Features

- **Search for books**: Use the Google Books API to search for books by title and author.
- **Summarize descriptions**: Summarize book descriptions using a pre-trained model (`t5-small`) to extract key information.
- **Find similar books**: Compare book descriptions using sentence embeddings to recommend similar books from a pre-loaded dataset.
- **Clickable links**: Display results with clickable download links (Libgen) for easy access to recommended books.

## Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Frontend framework for building the interactive web application.
- **Transformers**: Used for text summarization.
- **Sentence-Transformers**: Used for generating sentence embeddings.
- **Pandas**: Data manipulation and analysis.
- **NumPy**: Numerical operations.
- **Google Books API**: Retrieve book data by title and author.
- **Docker**: Containerization for both frontend and backend.
- **Kubernetes**: Orchestration for deploying the application.

## Architecture

The application consists of two main components:

1. **Frontend Server**:
   - Built using Streamlit.
   - Runs on port `8501`.
   - Connects to the backend server to fetch book recommendations.

2. **Backend Server**:
   - Built using Flask.
   - Runs on port `5000`.
   - Serves book data and recommendations by querying a CSV file containing a database of 500 popular books.

The frontend and backend communicate via REST API calls. The backend uses pre-computed sentence embeddings stored in the CSV file to find similar books.

## Repository Structure

- **app/**: Frontend Streamlit application
  - **app.py**: Main Streamlit web application.
  - **Dockerfile**: Container definition for the frontend.
  - **requirements.txt**: Frontend dependencies.
- **backend/**: Backend API service
  - **app.py**: Flask API for serving book data.
  - **book_embeddings.csv**: Book data with embeddings.
  - **Dockerfile**: Container definition for the backend.
  - **requirements.txt**: Backend dependencies.
- **k8s/**: Kubernetes manifests for deployment
  - **kustomization.yaml**: Kustomize configuration.
  - **frontend-deployment.yaml**: Frontend deployment configuration.
  - **frontend-service.yaml**: Frontend service configuration.
  - **backend-deployment.yaml**: Backend deployment configuration.
  - **backend-service.yaml**: Backend service configuration.
  - **configmap.yaml**: ConfigMap for application configuration.
  - **secret.yaml**: Secrets for API keys and sensitive data.
- **generate_embeddings.py**: Script to generate book embeddings.

## How to Replicate the Project

### Prerequisites

- Install **Kubernetes** on your system.
- Obtain a Google Books API key.

### Deployment Using Kubernetes

1. Clone the repository:
   ```bash
   git clone https://github.com/bennymestel/BookFinder_FinalProject.git
   cd BookFinder_FinalProject
   ```

2. Apply the Kubernetes manifests:
   ```bash
   kubectl apply -k k8s/
   ```

3. Access the application:
   - The frontend server will be available at `http://localhost:8501`.

### Notes

- The Docker images for the frontend and backend are pre-built and available on DockerHub under the `bennymestel` account:
  - Frontend: `bennymestel/book-finder-frontend`
  - Backend: `bennymestel/book-finder-backend`
- To generate new book embeddings, use the `generate_embeddings.py` script.
- Ensure your Google Books API key is stored securely in the `k8s/secret.yaml` file or as an environment variable.

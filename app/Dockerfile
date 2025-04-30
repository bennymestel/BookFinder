FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app.py .

# Include the CSV asfallback
COPY book_embeddings.csv .

# Expose the port your Streamlit app runs on
EXPOSE 8501

# Run Streamlit app when the container launches
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
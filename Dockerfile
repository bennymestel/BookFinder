FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app.py .
COPY book_embeddings_with_links.csv .

# Run app.py when the container launches
CMD ["python", "app.py"]
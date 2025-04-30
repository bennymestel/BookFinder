FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY csv_api.py .
COPY book_embeddings.csv .

# Expose port 5000 for the Flask API
EXPOSE 5000

CMD ["python", "csv_api.py"]

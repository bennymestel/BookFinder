FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .

# Add this line to copy the .streamlit directory with secrets
COPY .streamlit/ /app/.streamlit/

# Disable SSL verification
ENV PYTHONHTTPSVERIFY=0
ENV CURL_CA_BUNDLE=""
ENV REQUESTS_CA_BUNDLE=""
ENV SSL_CERT_FILE=""

# Create a Python startup file to disable SSL verification
RUN echo 'import ssl; ssl._create_default_https_context = ssl._create_unverified_context' > /app/ssl_disable.py
ENV PYTHONSTARTUP=/app/ssl_disable.py

# Copy the config.toml to the correct Streamlit config path
RUN mkdir -p /root/.streamlit
COPY .streamlit/config.toml /root/.streamlit/config.toml

# Expose Streamlit's default port
EXPOSE 8501

# Start the app (Streamlit will use config.toml automatically)
CMD ["streamlit", "run", "app.py"]
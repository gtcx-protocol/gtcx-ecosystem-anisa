# ANISA Production Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader punkt stopwords wordnet

# Copy application code
COPY src/ ./src/
COPY configs/ ./configs/
COPY training_data/ ./training_data/

# Set Python path
ENV PYTHONPATH=/app
ENV ANISA_PORT=8083

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8083/health')" || exit 1

# Copy alembic files
COPY alembic.ini .
COPY alembic/ ./alembic/

# Copy startup script
COPY scripts/startup.sh .
RUN chmod +x startup.sh

# Install postgresql client for pg_isready
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Run the application
CMD ["./startup.sh"]

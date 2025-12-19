# Use official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for pdfplumber (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app

# Expose port 5000 for Flask app
EXPOSE 5000

# Environment variables required for AI API keys
ENV OPENAI_API_KEY=""
ENV GOOGLE_API_KEY=""

# Start the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

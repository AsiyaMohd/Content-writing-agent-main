# Use official Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if any needed for pdfplumber or others)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt ./

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose Flask default port
EXPOSE 5000

# Set environment variable for production
ENV FLASK_ENV=production

# Use gunicorn to serve the app in production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

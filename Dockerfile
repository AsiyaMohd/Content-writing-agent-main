# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables to ensure output is flushed and to avoid .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies needed for pdfplumber and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement files first for layer caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application source code
COPY . /app/

# Expose the Flask default port
EXPOSE 5000

# Use gunicorn for production deployment
CMD ["gunicorn", "-w", "-b", "0.0.0.0:5000", "app:app"]

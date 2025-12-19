# Use official python slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for pdfplumber, docx, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    libxml2-dev \
    libxslt1-dev \
    antiword \
    unrtf \
    poppler-utils \
    pstotext \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install first for better layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose Flask default port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

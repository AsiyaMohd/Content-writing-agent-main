# Use official Python runtime base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements to install dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app source code
COPY . .

# Expose Flask port
EXPOSE 5000

# Use gunicorn as the server for production deployment
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

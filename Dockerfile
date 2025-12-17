# Use official Python runtime base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specification
COPY requirements.txt ./

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose port 5000 for Flask app
EXPOSE 5000

# Use gunicorn for production running
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

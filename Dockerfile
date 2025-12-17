# Use official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application source
COPY . /app/

# Expose port 5000 for Flask
EXPOSE 5000

# Use gunicorn to serve the app
CMD ["gunicorn", "--bind",  "0.0.0.0:5000", "app:app"]

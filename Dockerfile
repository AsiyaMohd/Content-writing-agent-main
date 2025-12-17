# Base image: official Python 3.11 slim image (modern version with security updates)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (for pdfplumber and other libs requiring build tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv and dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project code
COPY . /app/

# Expose port (Flask default 5000)
EXPOSE 5000

# Use gunicorn for production server
# CMD ["python", "app.py"] # Development run
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers", "1"]

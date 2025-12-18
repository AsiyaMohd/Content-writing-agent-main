# Use official Python image with slim variant
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy only requirements first to leverage caching
COPY requirements.txt ./

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy app source code to container
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Default environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

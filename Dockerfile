# Use official Python runtime image as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app source code
COPY . /app/

# Expose port 5000 for Flask
EXPOSE 5000

# Run the application with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

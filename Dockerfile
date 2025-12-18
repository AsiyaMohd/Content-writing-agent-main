# Dockerfile for Content-writing-agent-main Python Flask app

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app source code
COPY . /app/

# Expose port 5000
EXPOSE 5000

# Run using Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

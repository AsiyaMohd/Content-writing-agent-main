# Implementation Guide for Content-writing-agent-main

## Prerequisites
- Docker installed on local machine
- Docker Compose installed
- Python 3.11 installed (for local development without Docker)
- GitHub account (for using GitHub Actions CI/CD)

## Required GitHub Secrets
- If you add Docker image push functionality, configure secrets for Docker registry credentials (e.g., DOCKER_USERNAME, DOCKER_PASSWORD).

## Environment Variables
- FLASK_ENV: Set to "production" in the docker-compose.yml for running the app in production mode.

## Local Development Setup
1. Clone the repository
   ```bash
   git clone https://github.com/AsiyaMohd/Content-writing-agent-main.git
   cd Content-writing-agent-main
   ```
2. (Optional) Set up a Python virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask app
   ```bash
   python app.py
   ```

## Running with Docker

1. Build the Docker image
   ```bash
   docker build -t content-writing-agent .
   ```
2. Run the Docker container
   ```bash
   docker run -p 5000:5000 content-writing-agent
   ```

## Using Docker Compose

1. Start the app service
   ```bash
   docker-compose up --build
   ```

## Deployment
- The repository is configured with a GitHub Actions workflow for CI/CD.
- It builds the Docker image on pushes to the main branch.
- Add steps to push Docker images and deploy to your hosting provider in the workflow.

## Database Setup
- No database is required for this app.

## Troubleshooting
- Ensure ports are free on 5000 before starting the app.
- Check Docker daemon is running for Docker-based commands.
- Verify network connection and API keys for Langchain and OpenAI services required by the app.

## Documentation
- The app uses Flask as the web framework.
- Main entry point is app.py, which accepts PDF and text input to generate AI content.

# Implementation Guide for Content Writing Agent

## Prerequisites
- Docker and Docker Compose installed on your system
- Python 3.11 (for local development if not using Docker)
- GitHub account for CI/CD runs

## Environment Variables
- The application uses API keys for AI services which should be provided as environment variables.
- Create a `.env` file or set environment variables in your hosting platform or docker-compose environment.
  - Example:
    - OPENAI_API_KEY
    - GOOGLE_API_KEY (if using Google Gemini via LangChain)

## Setup and Running

### Using Docker
1. Build the Docker image:
```
docker build -t content-writing-agent .
```

2. Run the container:
```
docker run -p 5000:5000 --env-file .env content-writing-agent
```

### Using Docker Compose
1. Run the following command to start the service:
```
docker-compose up --build
```
This will start the app on port 5000.

### Local Development
1. Install dependencies:
```
pip install -r requirements.txt
```
2. Run the Flask app directly:
```
python app.py
```
3. Access the app at http://localhost:5000

## CI/CD Pipeline
- The included GitHub Actions workflow installs dependencies, runs lint checks, imports the app module, and builds the Docker image.
- This runs on pushes and pull requests to the `main` branch.

## Database and External Services
- This app does not use any external database or persistent service.
- It relies on external AI APIs which require proper API keys.

## Troubleshooting
- Ensure your environment variables for API keys are set correctly.
- Check Docker logs for errors with:
```
docker logs <container_id>
```
- For development issues, run Flask app without Docker in debug mode.

## Useful Links
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)


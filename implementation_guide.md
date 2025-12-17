# Implementation Guide for Content-writing-agent-main

## Prerequisites
- Docker
- Docker Compose
- GitHub account (for CI/CD)
- Docker Hub account (for Docker image push)
- Python 3.10 (for local development without Docker)

## Environment Variables
Please set the following environment variables in your deployment environment:
- `OPENAI_API_KEY`: Your OpenAI API key for access to language models

Additional environment variables may be required by LangChain or other components; refer to their documentation.

## Local Development Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/AsiyaMohd/Content-writing-agent-main.git
   cd Content-writing-agent-main
   ```
2. (Optional) Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set environment variables locally, e.g., create a `.env` file with your keys.
5. Run the Flask app:
   ```bash
   python app.py
   ```
6. Access the app at: http://localhost:5000

## Docker Setup and Run
1. Build the Docker image:
   ```bash
   docker build -t content-writing-agent .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 --env OPENAI_API_KEY=$OPENAI_API_KEY content-writing-agent
   ```
3. Open browser at http://localhost:5000

## Using Docker Compose
1. Build and start the service:
   ```bash
   docker-compose up --build
   ```
2. Compose file maps port 5000 and mounts code for local changes

## CI/CD
- The repository includes a GitHub Actions workflow that runs on push or pull request to main branch.
- Workflow installs dependencies, builds Docker image, and pushes it to Docker Hub.
- Use GitHub Secrets:
  - `DOCKERHUB_USERNAME`: Your Docker Hub username
  - `DOCKERHUB_TOKEN`: Your Docker Hub access token/password

## Deployment
- The Docker image pushed to Docker Hub can be deployed to any container platform.
- Customize deployment scripts or workflows as needed.

## Troubleshooting
- Ensure all environment variables are set
- Check Docker and Docker Compose versions
- View logs for errors: `docker logs <container_id>`
- For Flask errors, check console output

## Further Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [LangChain Documentation](https://docs.langchain.com/)

---

This guide covers local development, Docker usage, and CI/CD setup for the Content-writing-agent-main app.
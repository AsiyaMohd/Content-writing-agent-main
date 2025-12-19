# Implementation Guide for Content-writing-agent-main

## Prerequisites
- Docker 20.10+
- Docker Compose 1.29+
- Python 3.10 (for local development without Docker)
- GitHub account (for CI/CD)

## Environment Variables
- No explicit .env is used but you may create one for customization

## Local Development Setup
1. Clone the repo:
   ```sh
   git clone https://github.com/AsiyaMohd/Content-writing-agent-main.git
   cd Content-writing-agent-main
   ```
2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Flask app:
   ```sh
   python app.py
   ```
5. Access the app at `http://localhost:5000`

## Docker Setup

### Build and Run Docker Container
```sh
docker build -t content-writing-agent .
docker run -p 5000:5000 content-writing-agent
```

### Using Docker Compose
```sh
docker-compose up --build
```

## GitHub Actions CI/CD
- The workflow installs dependencies, runs lint, and builds Docker image on push/PR to main branch.
- Deployment steps are placeholder; customize based on deployment target.

## Application Details
- Flask-based web app serving frontend from `templates/` and static assets.
- Main logic in `app.py` invoking LangGraph agent for content generation.
- Supports PDF, TXT, DOCX file upload and parsing.

## Troubleshooting
- Ensure all dependencies installed.
- Use `docker logs <container>` for Docker container logs.
- Adjust port if 5000 is occupied.

## Further Enhancements
- Add proper environment variable configuration.
- Add unit/integration tests.
- Add real deployment steps in CI/CD workflow.

---

For further details, refer to the [README.md](README.md) file in the repo.
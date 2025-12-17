# Implementation Guide for Content Writing Agent

## Prerequisites
- Docker installed on your system
- Python 3.11 (for local dev)
- GitHub account to use CI/CD workflows
- API keys for OpenAI or Langchain services if applicable (user must provide these as environment variables)

## Environment Variables
This app may require the following environment variables to function properly (not explicitly defined in repo, verify with your deployed environment):
- OPENAI_API_KEY
- TAVILY_API_KEY (optional if search features used)

## Local Setup
1. Clone the repository:
```bash
git clone https://github.com/AsiyaMohd/Content-writing-agent-main.git
cd Content-writing-agent-main
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the Flask app locally:
```bash
flask run
```

Open http://localhost:5000 in your browser to access the app.

## Using Docker
1. Build the Docker image:
```bash
docker build -t content-writing-agent .
```

2. Run the container:
```bash
docker run -p 5000:5000 content-writing-agent
```

The app will be accessible at http://localhost:5000

## CI/CD Workflow
The GitHub Actions workflow (.github/workflows/cicd.yml) is configured to:
- Run on pushes and pull requests to main branch
- Setup Python 3.11
- Install dependencies
- Lint the code
- Build the Docker image

You can add deployment steps or tests as needed.

## Deployment
- The app Docker image can be deployed to any container platform (AWS ECS, Azure, GCP, Docker Hub, etc.)
- Make sure to supply required API keys and environment variables securely

## Troubleshooting
- If the app fails to start, ensure all dependencies are installed
- Check that environment variables are correctly set
- Check Docker container logs for errors

## Additional Notes
- The app listens on port 5000
- The app runs in debug mode by default; consider switching to production server (Gunicorn) for production deployments

## References
- Flask documentation: https://flask.palletsprojects.com/
- Docker documentation: https://docs.docker.com/
- GitHub Actions: https://docs.github.com/en/actions

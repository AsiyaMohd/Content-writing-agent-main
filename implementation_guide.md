# Implementation Guide for Content Writing Agent

## Overview
This repository contains a Python Flask web application that uses AI technologies to generate content based on user inputs and file uploads.

## Prerequisites
- Docker and docker-compose installed on your machine
- Python 3.11 (only if running locally without Docker)
- GitHub account to use CI/CD GitHub Actions
- OpenAI API key or other required API keys for Langchain and LangGraph

## Environment Variables
Create a `.env` file or set environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key for accessing AI models
- `TAVILY_API_KEY`: API key for web scraping tool (used in tools/search_tool.py)
- Any other keys required by Langchain or LangGraph agents

## Local Development Setup
1. Clone the repository

```bash
git clone https://github.com/AsiyaMohd/Content-writing-agent-main.git
cd Content-writing-agent-main
```

2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set environment variables

```bash
export OPENAI_API_KEY="your_openai_api_key"
export TAVILY_API_KEY="your_tavily_api_key"
```

5. Run the Flask app

```bash
python app.py
```

6. Access app at `http://localhost:5000`

## Using Docker

Build and run the app with Docker:

```bash
docker build -t content-writing-agent-main .
docker run -p 5000:5000 --env-file .env content-writing-agent-main
```

Or use docker-compose:

```bash
docker-compose up --build
```

## CI/CD Pipeline
- On each push or pull request to `main` branch, GitHub Actions will:
  - Checkout code
  - Setup Python
  - Install dependencies
  - Lint code with flake8
  - Run tests (currently placeholder)
  - Build Docker image
  - Deploy step placeholder for future deployment integration

## Troubleshooting
- Ensure API keys are set properly
- Check Docker service status if using Docker
- Logs can be viewed from Flask app console or GitHub Actions logs

## Notes
- No database service setup is needed
- The application is stateless and depends on API integrations

## References
- Flask documentation: https://flask.palletsprojects.com/
- Langchain: https://python.langchain.com/
- OpenAI API: https://platform.openai.com/docs/api-reference
- Docker: https://docs.docker.com/
- GitHub Actions: https://docs.github.com/en/actions

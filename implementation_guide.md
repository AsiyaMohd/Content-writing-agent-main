# Implementation Guide for Content-writing-agent-main

## Prerequisites
- Docker and Docker Compose installed on your system.
- Python 3.10 environment if running outside Docker.
- GitHub account to use CI/CD pipeline.
- API key for Tavily Search (set as TAVILY_API_KEY environment variable).

## Environment Variables
- `TAVILY_API_KEY`: Required for the search tool to function.

## Local Development Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/AsiyaMohd/Content-writing-agent-main.git
   cd Content-writing-agent-main
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables. Create a `.env` file in the project root with:
   ```
   TAVILY_API_KEY=your_api_key_here
   ```

5. Run the Flask app for development:
   ```bash
   flask run
   ```

## Using Docker
1. Build the Docker image:
   ```bash
   docker build -t content-writing-agent .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 --env TAVILY_API_KEY=your_api_key_here content-writing-agent
   ```

3. Alternatively, use Docker Compose to build and run:
   ```bash
   docker-compose up --build
   ```

## CI/CD Pipeline
- The GitHub Actions workflow triggers on push or pull request to the `main` branch.
- It checks out the code, sets up Python, installs dependencies, runs lint checks with flake8, builds the Docker image.
- No tests or deployment steps are currently implemented; modify the workflow to add deployment steps.

## Notes
- The web app listens on port 5000.
- The main entrypoint is `app.py`.
- Make sure to set the required environment variable TAVILY_API_KEY before running the app.

## Troubleshooting
- If the app cannot start, verify your API key and network connectivity.
- Check Docker logs if running inside containers.
- Ensure dependencies in requirements.txt are installed correctly.

## Future Considerations
- Add tests and integration with a deployment platform.
- Add database or caching layers if required.
- Improve security by managing secrets with GitHub Secrets or other vaults.

## Documentation
- The repository's README file contains limited info; refer to this guide for setup.
- The code uses LangChain and other AI tools, refer to upstream docs for advanced usage.

# LLM Debater 🚨

An interactive AI debate platform that enables different language models to engage in structured debates on user-defined topics. The platform features multiple LLM participants and optional judging functionality.

## Features

- Select different language models for debaters (llama2, mistral, neural-chat)
- Configure the number of debate rounds (1-5)
- Optional judging system with customizable judge model
- Real-time debate visualization with pro/con formatting
- Final verdict system for debate outcomes
- Docker support for easy deployment

## Prerequisites

- Docker and Docker Compose
- Access to an Ollama server for LLM inference
- Python 3.9+ (if running locally)

## Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd llm-debater
```

2. Configure the Ollama host in `docker-compose.yaml` (default: http://10.27.10.200:11434):
```yaml
environment:
  - OLLAMA_HOST=http://your-ollama-host:11434
```

3. Build and run the container:
```bash
docker-compose up --build
```

4. Access the application at `http://localhost:8505`

## Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Select models for both debaters from the dropdown menus
2. Choose the number of debate rounds (1-5)
3. Enable/disable the judging feature
4. If judging is enabled, select a model for the judge
5. Enter a debate topic
6. Click "Start Debate" to begin the session

## Environment Variables

- `OLLAMA_HOST`: URL of your Ollama server (default: http://10.27.10.200:11434)

## Project Structure

```
llm-debater/
├── app.py              # Main Streamlit application
├── Dockerfile          # Docker configuration
├── docker-compose.yaml # Docker Compose configuration
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Technical Details

- Built with Streamlit for the web interface
- Uses Ollama API for LLM inference
- Supports multiple LLM models:
  - llama2
  - mistral
  - neural-chat
- Implements custom CSS for debate visualization
- Features asynchronous message processing with sleep intervals

## Limitations

- Maximum of 5 debate rounds per session
- Requires active connection to an Ollama server
- Responses are limited to single sentences
- Fixed set of available LLM models

## License

MIT License
(c) 2025 Dave Rintoul

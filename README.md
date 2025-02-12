# AI Debate Arena 🎭

A dynamic web application that enables AI language models to engage in structured debates on user-defined topics. Built with Streamlit and Ollama, this platform facilitates real-time debates between different language models with optional judging and fact-checking capabilities.

## Features

- **Multi-Model Debates**: Choose different language models (llama2, mistral, neural-chat) for each debater
- **Configurable Rounds**: Set debate length from 1-5 rounds
- **Optional Judging**: Enable a third AI model to judge the debate and declare a winner
- **Fact Checking**: Optional fact-checking of debate statements by an AI model
- **Real-time Visualization**: Live debate display with pro/con formatting
- **Single-Sentence Responses**: Enforced concise arguments for clear debate flow
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Prerequisites

- Docker and Docker Compose
- Access to an Ollama server for LLM inference
- Python 3.9+ (if running locally)
- The following models available on your Ollama server:
  - llama2
  - mistral
  - neural-chat

## Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-debate-arena
```

2. Configure the Ollama host in `docker-compose.yaml`:
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

3. Set environment variables:
```bash
export OLLAMA_HOST=http://your-ollama-host:11434
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage Guide

1. **Configure Debaters**:
   - Select models for both Pro and Con positions
   - Choose the number of debate rounds (1-5)

2. **Optional Features**:
   - Enable/disable the judging feature
   - Enable/disable fact checking
   - Select models for judge and fact checker if enabled

3. **Start Debate**:
   - Enter a debate topic
   - Click "Start Debate"
   - Watch the debate unfold in real-time

4. **View Results**:
   - If judging is enabled, view the final verdict
   - If fact checking is enabled, see verification status for each statement

## Project Structure

```
ai-debate-arena/
├── app.py                  # Main Streamlit application
├── config.py              # Configuration settings
├── debate_manager.py      # Core debate logic
├── llm_service.py         # LLM API interaction
├── ui_components.py       # UI component definitions
├── styles.py             # Custom CSS styles
├── Dockerfile            # Docker configuration
├── docker-compose.yaml   # Docker Compose setup
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Configuration Options

Edit `config.py` to modify:
- Available LLM models
- Maximum number of debate rounds
- Default number of rounds
- Ollama host URL

## Limitations

- Limited to single-sentence responses for clarity
- Requires active connection to an Ollama server
- Maximum of 5 debate rounds per session
- Fixed set of available LLM models
- Fact checking accuracy depends on the model's capabilities

## License

MIT License
(c) 2025 Dave Rintoul

## Acknowledgments

- Built with Streamlit for web interface
- Uses Ollama for LLM inference
- UI inspired by modern debate formats

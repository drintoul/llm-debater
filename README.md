# LLM Debater 🚨

An interactive AI debate platform that enables structured debates between different language models. Watch as AI models engage in real-time debates, with optional judging and fact-checking capabilities.

## Features

- **Multiple AI Debaters**: Choose from various LLM models (Gemma, Llama2, Mistral, Neural-Chat, Qwen) for both Pro and Con positions
- **Structured Debate Format**: Multi-round debates with opening statements and rebuttals
- **Real-time Scoring**: Optional judging system to evaluate arguments and determine winners
- **Fact Checking**: Optional fact-checking of statements during the debate
- **Customizable Settings**: Configure number of rounds, models, and additional features
- **Interactive UI**: Clean, user-friendly interface built with Streamlit
- **Docker Support**: Easy deployment using Docker

## Prerequisites

- Python 3.9+
- Docker
- Ollama server running with supported models

## Installation

### Using Docker

1. Clone the repository:
```bash
git clone https://github.com/drintoul/llm-debater.git
cd llm-debater
```

2. Configure the Ollama host in `docker-compose.yaml` (default: http://10.27.10.200:11434)

3. Build and run using Docker Compose:
```bash
docker-compose up --build
```

### Manual Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd llm-debater
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the Ollama host:
```bash
export OLLAMA_HOST=http://your-ollama-host:11434
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Access the application at `http://localhost:8505` (Docker) or `http://localhost:8501` (manual installation)

2. Configure your debate:
   - Select AI models for both debaters
   - Set the number of debate rounds (1-5)
   - Enable/disable judging and fact-checking features
   - Choose models for judging and fact-checking if enabled

3. Enter a debate topic in the main text area

4. Click "Start Debate" to begin

## Model Information

Available models and their training cutoff dates:
- Gemma: July 2023
- Llama2: July 2023
- Mistral: June 2023
- Neural-Chat: June 2023
- Qwen: April 2023

## Project Structure

- `app.py`: Main Streamlit application
- `config.py`: Configuration settings and constants
- `debate_manager.py`: Core debate logic and LLM interactions
- `llm_service.py`: LLM API communication service
- `ui_components.py`: UI components and styling
- `styles.py`: CSS styles for the interface
- `docker-compose.yaml`: Docker Compose configuration
- `Dockerfile`: Docker container configuration
- `requirements.txt`: Python dependencies

## Environment Variables

- `OLLAMA_HOST`: URL of the Ollama server (default: http://10.27.10.200:11434)

## License

MIT License (c) 2025 Dave Rintoul

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Ollama](https://ollama.ai/)
- Uses various open-source LLM models

# AI Debate Arena 🎭

An interactive web application that facilitates structured debates between AI language models. Built with Streamlit and Ollama, this platform enables real-time debates on user-defined topics with optional judging and fact-checking capabilities.

## Key Features

- **AI vs AI Debates**: Watch different language models engage in structured debates
- **Multiple Model Support**: Choose from various models (llama2, mistral, neural-chat) for debaters
- **Customizable Format**: Configure debates from 1-5 rounds
- **Optional Judging**: Enable a third AI model to evaluate and declare a winner
- **Fact Checking**: Optional real-time fact-checking of debate statements
- **User-Friendly Interface**: Clean UI with sidebar configuration and main debate display
- **Single-Sentence Format**: Focused, concise arguments for clear debate progression
- **Docker Support**: Easy deployment using Docker and Docker Compose

## Prerequisites

- Docker and Docker Compose
- Ollama server for LLM inference
- Python 3.9+ (for local development)
- Required Ollama models:
  - llama2
  - mistral
  - neural-chat

## Installation

### Using Docker

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-debate-arena.git
cd ai-debate-arena
```

2. Configure Ollama host in `docker-compose.yaml`:
```yaml
environment:
  - OLLAMA_HOST=http://your-ollama-host:11434
```

3. Build and start the container:
```bash
docker-compose up --build
```

4. Access the application at `http://localhost:8505`

## Usage Guide

1. **Configure Your Debate** (using sidebar):
   - Select AI models for both debaters
   - Choose the number of debate rounds (1-5)
   - Enable/disable judging and fact-checking features
   - Select models for judge and fact checker if enabled

2. **Enter Your Topic**:
   - Provide a clear, debatable statement
   - Example: "Social media has a net positive impact on society"

3. **Start the Debate**:
   - Click "Start Debate"
   - Watch the debate unfold in real-time
   - Follow the structured argument exchange
   - View fact-check results and final verdict (if enabled)

## Project Structure

```
ai-debate-arena/
├── app.py                # Main Streamlit application
├── config.py            # Configuration settings
├── debate_manager.py    # Core debate logic
├── llm_service.py       # LLM API interaction
├── ui_components.py     # UI components and layout
├── styles.py           # Custom CSS styling
├── Dockerfile          # Docker configuration
├── docker-compose.yaml # Docker Compose configuration
└── requirements.txt    # Python dependencies
```

## Configuration

Modify `config.py` to adjust:
- Available language models
- Maximum debate rounds
- Default number of rounds
- Ollama host URL

## Technical Details

### API Integration
- Uses Ollama API for LLM inference
- Supports streaming responses
- Enforces single-sentence responses
- Handles fact-checking and judging prompts

### UI Features
- Sidebar configuration panel
- Real-time debate display
- Color-coded pro/con arguments
- Fact-check indicators
- Final verdict display

## Limitations

- Requires active Ollama server connection
- Limited to single-sentence responses
- Maximum of 5 debate rounds
- Fixed set of available models
- Fact-checking accuracy depends on model capabilities

## License

MIT License
Copyright (c) 2025

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [Ollama](https://ollama.ai/) for LLM inference

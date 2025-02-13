import os

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://10.27.10.200:11434')
AVAILABLE_MODELS = ["llama2", "mistral", "neural-chat", "gemma", "qwen"]

MODEL_CUTOFF_DATES = {
    "llama2": "July 2023",
    "mistral": "June 2023",
    "neural-chat": "June 2023",
    "gemma": "July 2023",
    "qwen": "April 2023"
}

MAX_ROUNDS = 5
DEFAULT_ROUNDS = 3

# Fact checking configuration
FACT_CHECK_MAX_TOKENS = 100  # Maximum tokens for fact check responses
FACT_CHECK_DETAILED = False   # Whether to provide detailed fact check explanations

import os

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://10.27.10.200:11434')
AVAILABLE_MODELS = ["gemma2:9b", "llama2:13b", "mistral:7b", "neural-chat:7b", "qwen2.5:14b"]

MODEL_CUTOFF_DATES = {
    "gemma2:9b": "July 2023",
    "llama2:13b": "July 2023",
    "mistral:7b": "June 2023",
    "neural-chat:7b": "June 2023",
    "qwen2.5:14b": "April 2023"
}

MAX_ROUNDS = 5
DEFAULT_ROUNDS = 3

# Fact checking configuration
FACT_CHECK_MAX_TOKENS = 100  # Maximum tokens for fact check responses
FACT_CHECK_DETAILED = False   # Whether to provide detailed fact check explanations

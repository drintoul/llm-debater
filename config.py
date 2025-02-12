import os

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://10.27.10.200:11434')
AVAILABLE_MODELS = ["llama2", "mistral", "neural-chat"]
MAX_ROUNDS = 5
DEFAULT_ROUNDS = 3

# Fact checking configuration
FACT_CHECK_MAX_TOKENS = 200  # Maximum tokens for fact check responses
FACT_CHECK_DETAILED = True   # Whether to provide detailed fact check explanations

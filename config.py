import json
import os

from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
AVAILABLE_MODELS = [m.strip() for m in os.getenv("AVAILABLE_MODELS", "").split(",") if m.strip()]

try:
    MODEL_CUTOFF_DATES = json.loads(os.getenv("MODEL_CUTOFF_DATES", "{}"))
except json.JSONDecodeError:
    MODEL_CUTOFF_DATES = {}

MAX_ROUNDS = int(os.getenv("MAX_ROUNDS", "5"))
DEFAULT_ROUNDS = int(os.getenv("DEFAULT_ROUNDS", "3"))

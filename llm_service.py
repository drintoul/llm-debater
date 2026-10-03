import json
import re
import time
import requests
from config import OLLAMA_HOST

class LLMService:
    TIMEOUT = 120
    RETRIES = 2  # one retry after the initial attempt

    @staticmethod
    def check_server_health():
        """Check if the Ollama server is accessible"""
        try:
            response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    @staticmethod
    def get_pulled_models():
        """Return the model names pulled on the Ollama server, or None if unreachable."""
        try:
            response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
            if response.status_code == 200:
                return [m.get("name", "") for m in response.json().get("models", [])]
        except requests.RequestException:
            pass
        return None

    @staticmethod
    def _post(prompt, model, stream):
        """POST to /api/generate, retrying once on timeouts/connection errors."""
        data = {"model": model, "prompt": prompt, "stream": stream}
        for attempt in range(LLMService.RETRIES):
            try:
                response = requests.post(
                    f"{OLLAMA_HOST}/api/generate",
                    json=data,
                    timeout=LLMService.TIMEOUT,
                    stream=stream,
                )
                response.raise_for_status()
                return response
            except (requests.Timeout, requests.ConnectionError):
                if attempt == LLMService.RETRIES - 1:
                    raise
                time.sleep(2)

    @staticmethod
    def _with_length(prompt, length):
        """Append the requested response-length instruction to a prompt."""
        if length == "sentence":
            return prompt + " IMPORTANT: Respond with exactly one sentence."
        if length == "paragraph":
            return prompt + " IMPORTANT: Respond with a short paragraph (3-4 sentences)."
        return prompt

    @staticmethod
    def get_response(prompt, model, length=None, fact_check=False):
        """Return the model's full response, or 'Error: ...' on failure."""
        prompt = LLMService._with_length(prompt, length)

        try:
            response = LLMService._post(prompt, model, stream=False)
            result = response.json()["response"].strip()
            return LLMService._cleanup(result, fact_check)
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def stream_response(prompt, model, length=None):
        """Yield response tokens as they arrive. On failure yields one 'Error: ...' chunk."""
        prompt = LLMService._with_length(prompt, length)

        try:
            response = LLMService._post(prompt, model, stream=True)
            for line in response.iter_lines():
                if line:
                    token = json.loads(line).get("response")
                    if token:
                        yield token
        except Exception as e:
            yield f"Error: {str(e)}"

    @staticmethod
    def _cleanup(result, fact_check=False):
        """Flatten line breaks, normalize fact-check labels, ensure terminal punctuation."""
        result = result.replace('\n', ' ').strip()

        if fact_check:
            result = LLMService._normalize_fact_check(result)

        if not result.endswith(('.', '!', '?')):
            result += '.'

        return result

    @staticmethod
    def _normalize_fact_check(result):
        """Ensure the response starts with a valid label: VERIFIED / PARTIALLY VERIFIED / UNVERIFIED."""
        label_map = {
            "VERIFIED": "VERIFIED:",
            "PARTIALLY VERIFIED": "PARTIALLY VERIFIED:",
            "UNVERIFIED": "UNVERIFIED:",
            "NOT VERIFIED": "UNVERIFIED:",
        }
        pattern = re.compile(
            r'\b(PARTIALLY\s+VERIFIED|UNVERIFIED|NOT\s+VERIFIED|VERIFIED)\s*:',
            re.IGNORECASE
        )

        match = pattern.search(result)
        if match:
            label = label_map[re.sub(r'\s+', ' ', match.group(1)).upper()]
            content = pattern.sub("", result[match.end():]).strip()
            return f"{label} {content}"

        return "UNVERIFIED: " + result

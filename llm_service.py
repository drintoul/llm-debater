import requests
from config import OLLAMA_HOST

class LLMService:
    @staticmethod
    def check_server_health():
        """Check if the Ollama server is accessible"""
        try:
            response = requests.get(f"{OLLAMA_HOST}/api/tags")
            return response.status_code == 200
        except requests.RequestException:
            return False

    @staticmethod
    def get_response(prompt, model):
        url = f"{OLLAMA_HOST}/api/generate"
        data = {
            "model": model,
            "prompt": prompt + " IMPORTANT: Respond with exactly one sentence.",
            "stream": False
        }

        try:
            response = requests.post(url, json=data)
            result = response.json()["response"].strip()

            # Clean up any line breaks and extra spaces
            result = result.replace('\n', ' ').strip()

            # For fact checking responses, ensure proper label format
            if "fact check" in prompt.lower():
                valid_labels = ["VERIFIED:", "PARTIALLY VERIFIED:", "UNVERIFIED:"]

                # Find the first valid label in the response
                first_label = None
                first_label_pos = float('inf')

                for label in valid_labels:
                    pos = result.upper().find(label)
                    if pos != -1 and pos < first_label_pos:
                        first_label = label
                        first_label_pos = pos

                if first_label:
                    # Keep only the content after the first valid label
                    content_after_label = result[first_label_pos + len(first_label):].strip()
                    # Remove any other labels that might appear in the content
                    for label in valid_labels:
                        content_after_label = content_after_label.replace(label, "")
                    result = first_label + " " + content_after_label
                else:
                    # If no valid label found, add UNVERIFIED as default
                    result = "UNVERIFIED: " + result

            # Ensure proper sentence punctuation
            if not result.endswith(('.', '!', '?')):
                result += '.'

            return result
        except Exception as e:
            return f"Error: {str(e)}"

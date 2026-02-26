import requests

URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def generate_response(prompt: str):

        try:
            response = requests.post(
                URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=300
            )

            response.raise_for_status()  # Raise an error for bad status codes

            data = response.json()

            return data.get("response", "no response from model")

        except requests.exceptions.Timeout:
            return "model Timeout — Try again"

        except requests.exceptions.ConnectionError:
            return "Ollama server is not running."

        except Exception as e:
            return f"Unexpected error: {str(e)}"

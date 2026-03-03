import os

import requests

URL = "http://localhost:11434/api/generate"


def _normalize_ollama_model_name(model_name: str) -> str:
    return model_name.split(":", 1)[0].strip().lower()


def _is_embedding_model(model_name: str) -> bool:
    normalized = _normalize_ollama_model_name(model_name)
    embedding_markers = ("embed", "embedding", "nomic-embed")
    return any(marker in normalized for marker in embedding_markers)


def _get_installed_ollama_models() -> list[str]:
    response = requests.get("http://localhost:11434/api/tags", timeout=15)
    response.raise_for_status()
    payload = response.json() or {}
    models = payload.get("models", [])
    return [model.get("name", "") for model in models if model.get("name")]


def _resolve_generation_model() -> str:
    requested = os.getenv("OLLAMA_GENERATION_MODEL", "mistral").strip()
    requested_base = _normalize_ollama_model_name(requested)

    installed = _get_installed_ollama_models()
    if not installed:
        return requested

    for model_name in installed:
        if _normalize_ollama_model_name(model_name) == requested_base:
            return model_name

    generation_candidates = [name for name in installed if not _is_embedding_model(name)]
    if generation_candidates:
        return generation_candidates[0]

    return requested


def _build_generate_payload(prompt: str, model_name: str, num_predict: int) -> dict:
    return {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": num_predict,
        },
    }


def generate_response(prompt: str):

        try:
            model_name = _resolve_generation_model()
            connect_timeout = int(os.getenv("OLLAMA_CONNECT_TIMEOUT_SECONDS", "15"))
            read_timeout = int(os.getenv("OLLAMA_READ_TIMEOUT_SECONDS", "900"))
            first_num_predict = int(os.getenv("OLLAMA_NUM_PREDICT", "1800"))
            retry_num_predict = int(os.getenv("OLLAMA_NUM_PREDICT_RETRY", "900"))

            response = requests.post(
                URL,
                json=_build_generate_payload(prompt, model_name, first_num_predict),
                timeout=(connect_timeout, read_timeout)
            )

            response.raise_for_status()  # Raise an error for bad status codes

            data = response.json()

            return data.get("response", "no response from model")

        except requests.exceptions.Timeout:
            try:
                model_name = _resolve_generation_model()
                connect_timeout = int(os.getenv("OLLAMA_CONNECT_TIMEOUT_SECONDS", "15"))
                retry_read_timeout = int(os.getenv("OLLAMA_READ_TIMEOUT_RETRY_SECONDS", "1200"))
                retry_num_predict = int(os.getenv("OLLAMA_NUM_PREDICT_RETRY", "900"))

                retry_response = requests.post(
                    URL,
                    json=_build_generate_payload(prompt, model_name, retry_num_predict),
                    timeout=(connect_timeout, retry_read_timeout)
                )
                retry_response.raise_for_status()
                retry_data = retry_response.json()
                return retry_data.get("response", "no response from model")
            except requests.exceptions.Timeout:
                return "model Timeout — Try again"
            except Exception as e:
                return f"Unexpected error: {str(e)}"

        except requests.exceptions.ConnectionError:
            return "Ollama server is not running."

        except Exception as e:
            return f"Unexpected error: {str(e)}"

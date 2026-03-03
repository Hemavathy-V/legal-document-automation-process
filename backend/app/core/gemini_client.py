import os
from typing import Iterable, Optional, Set

import google.generativeai as genai
from dotenv import load_dotenv

from backend.app.core.logger import get_logger


load_dotenv()
logger = get_logger(__name__)


def _normalize_model_name(model_name: Optional[str]) -> str:
    if not model_name:
        return ""
    normalized = model_name.strip()
    if normalized.startswith("models/"):
        normalized = normalized.split("models/", 1)[1]
    return normalized


def _get_available_generation_models() -> Set[str]:
    available: Set[str] = set()
    try:
        for model in genai.list_models():
            methods: Iterable[str] = getattr(model, "supported_generation_methods", []) or []
            if "generateContent" in methods:
                available.add(_normalize_model_name(getattr(model, "name", "")))
    except Exception as exc:
        logger.warning(f"Unable to list Gemini models. Falling back to configured/default model. Reason: {exc}")
    return available


def _resolve_model_name(requested_model: str, available_models: Set[str]) -> str:
    preferred_models = [
        _normalize_model_name(requested_model),
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro",
    ]

    ordered_candidates = [model for model in preferred_models if model]
    if not available_models:
        return ordered_candidates[0]

    for candidate in ordered_candidates:
        if candidate in available_models:
            return candidate

    return sorted(available_models)[0]


def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    requested_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    genai.configure(api_key=api_key)
    available_models = _get_available_generation_models()
    resolved_model = _resolve_model_name(requested_model, available_models)

    if _normalize_model_name(requested_model) != resolved_model:
        logger.warning(
            f"Configured Gemini model '{requested_model}' is unavailable. "
            f"Using fallback model '{resolved_model}'."
        )
    else:
        logger.info(f"Using Gemini model '{resolved_model}'")

    return genai.GenerativeModel(resolved_model)

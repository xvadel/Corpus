from backend.providers.base import LLMProvider
from backend.providers.gemini import GeminiProvider
from backend.providers.groq_provider import GroqProvider
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def get_provider(provider_name: str = None) -> LLMProvider:
    """
    Factory function to retrieve the configured LLMProvider.
    If provider_name is not supplied, it is read from the central config.toml.
    """
    if not provider_name:
        provider_name = "groq"  # Default fallback
        config_path = PROJECT_ROOT / "config.toml"
        if config_path.exists():
            try:
                import tomllib
                with open(config_path, "rb") as f:
                    config = tomllib.load(f)
                provider_name = config.get("ai_coach", {}).get("provider", "groq")
            except Exception:
                pass
    
    provider_name = provider_name.lower().strip()
    if provider_name == "groq":
        model_name = "llama-3.3-70b-versatile"
        config_path = PROJECT_ROOT / "config.toml"
        if config_path.exists():
            try:
                import tomllib
                with open(config_path, "rb") as f:
                    config = tomllib.load(f)
                model_name = config.get("ai_coach", {}).get("model", model_name)
            except Exception:
                pass
        return GroqProvider(model_name=model_name)
    elif provider_name == "openai":
        from backend.providers.openai import OpenAIProvider
        model_name = "gpt-4o-mini"
        config_path = PROJECT_ROOT / "config.toml"
        if config_path.exists():
            try:
                import tomllib
                with open(config_path, "rb") as f:
                    config = tomllib.load(f)
                model_name = config.get("ai_coach", {}).get("model", model_name)
            except Exception:
                pass
        return OpenAIProvider(model_name=model_name)
    else:
        model_name = "gemini-3.5-flash"
        config_path = PROJECT_ROOT / "config.toml"
        if config_path.exists():
            try:
                import tomllib
                with open(config_path, "rb") as f:
                    config = tomllib.load(f)
                model_name = config.get("ai_coach", {}).get("model", model_name)
            except Exception:
                pass
        return GeminiProvider(model_name=model_name)

__all__ = ["LLMProvider", "GeminiProvider", "GroqProvider", "get_provider"]

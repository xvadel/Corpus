import os
from pathlib import Path
from backend.providers.base import LLMProvider

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class GeminiProvider(LLMProvider):
    def __init__(self, model_name: str = "gemini-3.5-flash"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            import google.generativeai as genai
            
            # Load environment variables if not loaded
            try:
                import dotenv
                dotenv.load_dotenv(PROJECT_ROOT / ".env")
            except ImportError:
                pass
                
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key or api_key == "your_gemini_api_key_here":
                raise ValueError("GEMINI_API_KEY environment variable is not set or is placeholder.")
            
            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel(self.model_name)
        return self._model

    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Check if there is an issue with API key or quota
            print(f"Gemini generation error: {e}")
            raise e

import os
from pathlib import Path
from backend.providers.base import LLMProvider

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class OpenAIProvider(LLMProvider):
    def __init__(self, model_name: str = "gpt-4o-mini", api_key: str = None):
        self.model_name = model_name
        self.api_key = api_key
        self._client = None

    @property
    def client(self):
        if self._client is None:
            from openai import OpenAI
            
            # Load environment variables if not loaded
            try:
                import dotenv
                dotenv.load_dotenv(PROJECT_ROOT / ".env")
            except ImportError:
                pass
                
            key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not key or key == "your_openai_api_key_here":
                raise ValueError("OPENAI_API_KEY environment variable is not set or is placeholder.")
            
            self._client = OpenAI(api_key=key)
        return self._client

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI generation error: {e}")
            raise e

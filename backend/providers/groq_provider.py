import os
import json
import time
import urllib.request
import urllib.error
import re
from pathlib import Path
from backend.providers.base import LLMProvider

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class GroqProvider(LLMProvider):
    def __init__(self, model_name: str = "llama-3.3-70b-versatile", max_retries: int = 5, initial_backoff: float = 2.0):
        self.model_name = model_name
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.api_key = None

    def _get_api_key(self):
        if self.api_key is None:
            # Load environment variables if not loaded
            try:
                import dotenv
                dotenv.load_dotenv(PROJECT_ROOT / ".env")
            except ImportError:
                pass
                
            self.api_key = os.getenv("GROQ_API_KEY")
            if not self.api_key or self.api_key == "your_groq_api_key_here":
                raise ValueError("GROQ_API_KEY environment variable is not set or is placeholder.")
        return self.api_key

    def generate(self, prompt: str) -> str:
        api_key = self._get_api_key()
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        # Request object
        req_data = json.dumps(data).encode("utf-8")

        backoff = self.initial_backoff
        for attempt in range(self.max_retries + 1):
            req = urllib.request.Request(
                url, 
                data=req_data, 
                headers=headers,
                method="POST"
            )
            try:
                with urllib.request.urlopen(req) as response:
                    res_data = response.read().decode("utf-8")
                    res_json = json.loads(res_data)
                    return res_json["choices"][0]["message"]["content"]
            except urllib.error.HTTPError as e:
                # Catch rate limits (429) or transient server errors (500, 502, 503, 504)
                if e.code in (429, 500, 502, 503, 504):
                    if attempt == self.max_retries:
                        print(f"Groq API error on final attempt: {e.code} {e.reason}")
                        raise e
                    
                    # Try to read and parse the response body first before we lose it
                    wait_time = backoff
                    try:
                        body = e.read().decode("utf-8")
                        body_json = json.loads(body)
                        message = body_json.get("error", {}).get("message", "")
                        if "try again in" in message:
                            match = re.search(r"try again in ([\d\.]+)s", message)
                            if match:
                                wait_time = float(match.group(1)) + 0.5  # add a safety buffer
                    except Exception:
                        # If reading body fails, check headers for Retry-After
                        retry_after = e.headers.get("Retry-After")
                        if retry_after:
                            try:
                                wait_time = float(retry_after)
                            except ValueError:
                                pass
                    
                    print(f"\n[Groq] Rate limited/Server error ({e.code}). Retrying in {wait_time:.2f} seconds (attempt {attempt + 1}/{self.max_retries})...")
                    time.sleep(wait_time)
                    backoff *= 2
                else:
                    # Non-retryable error
                    print(f"\nGroq API HTTP Error: {e.code} {e.reason}")
                    try:
                        print(e.read().decode("utf-8"))
                    except Exception:
                        pass
                    raise e
            except Exception as e:
                if attempt == self.max_retries:
                    print(f"\nGroq API unexpected error on final attempt: {e}")
                    raise e
                print(f"\n[Groq] Unexpected error: {e}. Retrying in {backoff:.2f} seconds...")
                time.sleep(backoff)
                backoff *= 2

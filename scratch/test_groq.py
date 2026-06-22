import os
import json
import urllib.request
import urllib.error
from pathlib import Path

# Load env variables
PROJECT_ROOT = Path(__file__).resolve().parent.parent
try:
    import dotenv
    dotenv.load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

api_key = os.getenv("GROQ_API_KEY")
print(f"GROQ_API_KEY: {'set' if api_key else 'not set'}")
if api_key:
    print(f"Key starts with: {api_key[:10]}...")

# We'll try llama-3.3-70b-versatile or llama3-8b-8192
model = "llama-3.3-70b-versatile"
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
data = {
    "model": model,
    "messages": [
        {"role": "user", "content": "Hello! What is your name and model name?"}
    ],
    "temperature": 0.0
}

req = urllib.request.Request(
    url, 
    data=json.dumps(data).encode("utf-8"), 
    headers=headers,
    method="POST"
)

try:
    with urllib.request.urlopen(req) as response:
        res_data = response.read().decode("utf-8")
        res_json = json.loads(res_data)
        print("Success!")
        print(res_json["choices"][0]["message"]["content"])
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code} {e.reason}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")

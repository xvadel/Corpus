import os
import google.generativeai as genai
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
try:
    import dotenv
    dotenv.load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

api_key = os.getenv("GEMINI_API_KEY")
print(f"Using API Key (first 10 chars): {api_key[:10] if api_key else 'None'}")
genai.configure(api_key=api_key)

try:
    print("Listing models:")
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"  {m.name}")
            
    # Try gemini-3.5-flash
    print("\nTrying generate content with gemini-3.5-flash...")
    model = genai.GenerativeModel('gemini-3.5-flash')
    response = model.generate_content("Hello! What is your name?")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error testing Gemini: {e}")

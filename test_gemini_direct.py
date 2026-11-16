 
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load API key from .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

# Create Gemini client with a longer timeout
client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 120000}
)

print("Connecting to Gemini...", flush=True)

# Send a simple test request
response = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain Agentic AI in three simple sentences."
)

print("\nGemini Response:")
print(response.output_text)

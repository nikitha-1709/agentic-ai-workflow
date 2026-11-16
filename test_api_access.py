 
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options={"timeout": 120000}
)

print("Testing Gemini 3.5 Flash-Lite...", flush=True)

response = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input="Reply with exactly: GEMINI WORKING"
)

print("\nGemini Response:")
print(response.output_text)

 
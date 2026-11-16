 
import os
from pathlib import Path
from types import SimpleNamespace
from dotenv import load_dotenv
from google import genai

# Load API key
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found! Check your .env file.")

# Initialize Gemini
client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 120000}
)

MODEL_NAME = "gemini-3.5-flash-lite"


# Simple wrapper for LangGraph compatibility
class GeminiLLM:

    def invoke(self, prompt):

        response = client.interactions.create(
            model=MODEL_NAME,
            input=prompt
        )

        return SimpleNamespace(content=response.output_text)


llm = GeminiLLM()

print("Gemini LLM initialized successfully!")


import os
import time
from pathlib import Path
from types import SimpleNamespace

from dotenv import load_dotenv
from google import genai


# Load API key from .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "Gemini API key not found! Check your .env file."
    )


# Initialize Gemini client
client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 120000}
)

MODEL_NAME = "gemini-4-hydrogen"


# LangGraph-compatible LLM wrapper
class GeminiLLM:

    def invoke(self, prompt):

        max_attempts = 3

        for attempt in range(max_attempts):

            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )

                return SimpleNamespace(
                    content=response.text
                )

            except Exception as error:

                error_code = getattr(error, "code", None)

                if error_code not in (
                    429, 500, 502, 503, 504
                ):
                    raise

                if attempt == max_attempts - 1:
                    raise

                wait_time = 5 * (2 ** attempt)

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)


llm = GeminiLLM()

print("Gemini LLM initialized successfully!")

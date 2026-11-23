import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# config.env ko import kar (isi folder se, chahe script kahin se bhi chale)
load_dotenv(Path(__file__).parent / "config.env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def aiProcess(command):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=command,
                config={"system_instruction": "You are Friday, a virtual assistant. Answer in 1-2 short sentences."},
            )
            return response.text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(2)
    return "Sorry sir, the AI server is busy right now"


if __name__ == "__main__":
    print(aiProcess("What is coding?"))
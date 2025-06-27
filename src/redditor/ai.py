import os
from typing import Optional
import cohere
import dotenv
from pathlib import Path


DOTENV_FILE: Path = Path(__file__).parent.parent.parent / ".env" 
dotenv.load_dotenv(DOTENV_FILE, override=True) # Load environment variables from .env file

COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
co = cohere.ClientV2(COHERE_API_KEY)

def expound_title(title: str) -> Optional[str]:
    try:
        response: cohere.Generation = co.chat(
            model='command-a-03-2025',
            messages=[{"role": "user","content": f"Expound on this this Reddit post title in one short paragraph:\n{title}"}],
            max_tokens=64,
            temperature=0.5
        )
        return response.model_dump()["message"]["content"][0]["text"].strip()
    
    except Exception as e:
        print(f"Error generating expounded title: {e}")
        return None        


if __name__ == "__main__":
    title = "Why is the sky blue?"
    expounded = expound_title(title)
    print(f"Original Title: {title}")
    print(f"Expounded Title: {expounded}")
    
    print("🐬")
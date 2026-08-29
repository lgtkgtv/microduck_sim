import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai

def test_connection():
    # Target the global .env file located at ~/agy_projects/.env
    global_env_path = Path.home() / "agy_projects" / ".env"

    print(f"📁 Loading environment keys from: {global_env_path}")

    if global_env_path.exists():
        load_dotenv(dotenv_path=global_env_path)
    else:
        print(f"❌ Error: No .env file found at {global_env_path}")
        sys.exit(1)

    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found inside the loaded .env file!")
        sys.exit(1)

    print("📡 Initializing Google GenAI Client...")
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Respond with exactly the word: ONLINE',
        )
        print(f"✅ Connection Successful! Response: {response.text.strip()}")
        
    except Exception as e:
        print(f"❌ Connection Failed: {str(e)}")

if __name__ == "__main__":
    test_connection()

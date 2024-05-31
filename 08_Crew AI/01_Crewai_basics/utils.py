from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_serper_api_key():
    return os.getenv("SERPER_API_KEY")

def get_gemini_api_key():
    return os.getenv("GOOGLE_API_KEY")

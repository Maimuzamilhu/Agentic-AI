import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('API_KEY')

# Configure the genai library with the API key
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

class Website:
    def __init__(self, url):
        self.url = url
        self.content = self._fetch_content()

    def _fetch_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            # Limit content length to avoid exceeding token limits
            max_length = 10000  # Adjust this as needed
            return response.text[:max_length]
        except requests.RequestException as e:
            return f"Error fetching content: {str(e)}"

def messages_for(website):
    return [
        {"role": "user", "parts": ["Summarize the following website content:"]},
        {"role": "user", "parts": [website.content]}
    ]

def summarize(url):
    website = Website(url)
    input_prompt = messages_for(website)
    try:
        # Generate the summary
        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        return f"Error during summarization: {str(e)}"

def display_summary(url):
    summary = summarize(url)
    print("\nSummary:\n", summary)

# Example usage
if __name__ == "__main__":
    url = "https://ai.google.dev/gemini-api/docs/api-key"
    display_summary(url)

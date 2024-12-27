import pathlib
import textwrap
import time
from dotenv import load_dotenv
import os
import google.generativeai as genai
import google.ai.generativelanguage as glm
import requests
from IPython import display
from IPython.display import Markdown

load_dotenv()
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
#FINHUB_KEY = os.getenv("FINHUB_KEY")

api_key = os.getenv('API_KEY')

# Configure Gemini API
genai.configure(api_key=api_key)

# 01 - creating a custom function
def fetch_alpha_vantage_news():
    """Fetch news from Alpha Vantage"""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "topics": "financial_markets",
        "apikey": ALPHA_VANTAGE_KEY
    }

    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Error fetching Alpha Vantage news: {e}")
        return None

# initialize the model
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    generation_config={
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    },
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ],
)

# Start a chat
chat = model.start_chat(history=[])

# Send a message to the chat
response = chat.send_message('You are a financial assistant. Provide the latest news on the stock market.')
print(response.text)

# Ask for the latest news
response = chat.send_message('What\'s the latest news on the stock market?')
print(response.text)



"""if more than one api is used then after using we have to combine both like this

def analyze_news_with_gemini(alpha_news, fmp_news):
    Use Gemini to analyze and summarize stock news
    combined_articles = []

    if alpha_news and isinstance(alpha_news, dict):
        for article in alpha_news.get("feed", []):
            if isinstance(article, dict):
                title = article.get("title", "No Title")
                summary = article.get("summary", "No summary available")
                combined_articles.append(f"Alpha Vantage: {title} - {summary}")

    if fmp_news and isinstance(fmp_news, list):
        for article in fmp_news:
            if isinstance(article, dict):
                title = article.get("title", "No Title")
                summary = article.get("summary", "No summary available")
                combined_articles.append(f"FMP: {title} - {summary}")
"""
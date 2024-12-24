import os
import requests
import json
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import google.generativeai as genai
import time

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

# Configure Gemini API
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel(model_name='gemini-pro')

# Headers for HTTP requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class Website:
    """
    A utility class to represent a Website with text and links scraped from it.
    """

    def __init__(self, url):
        self.url = url
        self.base_url = url if url.endswith("/") else url + "/"  # Ensure URL ends with a slash
        response = requests.get(url, headers=headers)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')  # Parse HTML content
        self.title = soup.title.string if soup.title else "No title found"

        # Extract text content
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):  # Remove irrelevant tags
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""

        # Extract and clean links
        links = [link.get('href') for link in soup.find_all('a', href=True)]
        self.links = [self.resolve_link(link) for link in links if link]

    def resolve_link(self, link):
        """Convert relative URLs to absolute URLs."""
        if link.startswith("http") or link.startswith("www"):
            return link
        return os.path.join(self.base_url, link.lstrip('/'))

    def get_contents(self):
        """Return website contents."""
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"


def get_links_user_prompt(website):
    """Generate a user prompt based on the website's links."""
    user_prompt = f"Here is the list of links on the website of {website.url}:\n"
    user_prompt += "Please decide which of these are relevant web links for a brochure about the company.\n"
    user_prompt += "Respond with the full HTTPS URL in JSON format. Exclude Terms of Service, Privacy, and email links.\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


def extract_json(text):
    """Extract JSON from mixed text response."""
    match = re.search(r'\{.*\}', text, re.DOTALL)  # Matches the first JSON block
    if match:
        return match.group(0)
    return None


def get_links(url, retries=3):
    """Analyze links using Gemini AI with retry logic."""
    website = Website(url)
    prompt = f"""
You are provided with a list of links found on a webpage. 
Decide which of the links are most relevant to include in a brochure about the company, 
such as links to an About page, Company page, or Careers/Jobs pages.

Respond in JSON format:
{{
    "links": [
        {{"type": "about page", "url": "https://example.com/about"}},
        {{"type": "careers page", "url": "https://example.com/careers"}}
    ]
}}

Links on the page:
{get_links_user_prompt(website)}
"""

    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)

            # Attempt to extract JSON
            json_text = extract_json(response.text)
            if json_text:
                return json.loads(json_text)

            # Log and retry if parsing fails
            print(f"Attempt {attempt + 1}: Failed to parse JSON. Retrying...")
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error - {str(e)}. Retrying...")
        time.sleep(2)

    return {"error": "Failed to get valid response after retries."}


# Example: Analyze links from HuggingFace
duet = Website("https://duet.edu.pk/")
#print(duet.links)

result = get_links("https://duet.edu.pk/")
#print(result)

def get_all_details(url):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = get_links(url)
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result

print(get_all_details("https://duet.edu.pk/"))

system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt

def extract_json(text):
    """Extract JSON from mixed text responses."""
    match = re.search(r'\{.*\}', text, re.DOTALL)  # Matches the first JSON block
    if match:
        return match.group(0)
    return None

# --- Gemini Function ---
def create_brochure(company_name, url):
    """Generates a company brochure using Gemini API."""
    prompt = get_brochure_user_prompt(company_name, url)

    try:
        # Send the prompt to Gemini
        response = model.generate_content(prompt)


        # Print the streamed content
        print("\nGenerating Brochure...\n")
        for chunk in response:
            print(chunk.text, end="", flush=True)  # Flush to ensure streaming behavior


    except Exception as e:
        print(f"Error: {str(e)}")


# --- Example Usage ---
company_name = "dawood university"
url = "https://duet.edu.pk/"
create_brochure(company_name, url)

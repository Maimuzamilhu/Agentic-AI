import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

# System message setup
system_message = (
    "You are a helpful assistant for an Airline called FlightAI. "
    "Give short, courteous answers, no more than 1 sentence. "
    "Always be accurate. If you don't know the answer, say so."
)



# Function implementation
def get_ticket_price(destination_city: str):
    # Ticket price data
    ticket_prices = {
        "london": "$799",
        "paris": "$899",
        "tokyo": "$1400",
        "berlin": "$499"
    }

    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")

model = genai.GenerativeModel(
    model_name='gemini-pro',
    tools=[get_ticket_price] # list of all available tools
)
# 03 model in chat mode for function calling
chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message(' I want to visit in tokyo what will be the expense?')
print(response.text)

response = chat.send_message('what is the ticket price for Berlin?')
print(response.text)

for content in chat.history:
    part = content.parts[0]
    print(content.role, "->", type(part).to_dict(part))
    print('-'*80)
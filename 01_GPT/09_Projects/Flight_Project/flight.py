from openai import OpenAI
import json
from dotenv import find_dotenv , load_dotenv
import requests #to fetch
import os

#Client
client : OpenAI = OpenAI()



#Create Assistant
assistant = client.beta.assistants.create(
    instructions="You are a helpful assistant. If you are asked about a flight, use the flight number with the provided get_flight_details function to get information about the flight, then answer the user's question with that data exclusively.",
    model="gpt-3.5-turbo-1106",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_flight_details",
                "description": "get details about a flight",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flight_number": {
                            "type": "string",
                            "description": "The flight number"
                        }
                    },
                    "required": ["flight_number"]
                }
            }
        }
    ]
)


    
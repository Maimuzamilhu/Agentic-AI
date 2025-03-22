import chainlit as cl
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.tool import function_tool



load_dotenv(find_dotenv())
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Provider
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Config
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Custom tools
@function_tool("get_weather")
def get_weather(location: str, unit: str = "C") -> str:
  """
  Fetch the weather for a given location, returning a short description.
  """
  # Example logic
  return f"The weather in {location} is 22 degrees {unit}."

@function_tool("piaic_student_finder")
def student_finder(student_roll: int) -> str:
  """
  find the PIAIC student based on the roll number
  """
  data = {1: "Qasim",
          2: "Sir Zia",
          3: "Daniyal"}

  return data.get(student_roll, "Not Found")




# Global Agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful Assistant.",
    model=model,
    tools=[get_weather, student_finder], # add tools here
)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello, I am your Assistant Muzzamil. What can I do for you?").send()


@cl.on_message
async def main(message: cl.Message):
    # Retrieve the chat history from the session.
    history = cl.user_session.get("history") or []

    # Append user message to history
    history.append({"role": "user", "content": message.content})
    cl.user_session.set("history", history)

    # Initialize a new message for the assistant's response
    msg = cl.Message(content="")
    await msg.send()

    # Run the agent with streaming
    result = Runner.run_streamed(agent, history, run_config=config)

    # Stream the response token by token
    async for event in result.stream_events():
        if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
            token = event.data.delta
            await msg.stream_token(token)

    # After streaming is complete, append the complete assistant message to history
    history.append({"role": "assistant", "content": msg.content})
    cl.user_session.set("chat_history", history)
import chainlit as cl
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

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

# Global Agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful Assistant.",
    model=model
)


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello, I am your Assistant Muzzamil. What can I do for you?").send()


@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history", [])

    # Append user message to history
    user_message = {"role": "user", "content": message.content}
    history.append(user_message)
    cl.user_session.set("history", history)

    # Run agent with entire history
    result = await Runner.run(
        agent,
        input=history,
        run_config=config
    )

    # Append assistant response to history
    assistant_message = {"role": "assistant", "content": result.final_output}
    history.append(assistant_message)
    cl.user_session.set("history", history)

    await cl.Message(content=result.final_output).send()
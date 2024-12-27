# Ensure your VertexAI credentials are configured

from langchain_google_vertexai import ChatVertexAI

model = ChatVertexAI(model="gemini-1.5-flash")

model.invoke("Hello, world!")
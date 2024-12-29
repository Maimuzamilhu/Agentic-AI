from langchain_google_genai import ChatGoogleGenerativeAI
import os
from crewai_tools import PDFSearchTool
from crewai_tools import tool
from crewai import Crew, Task, Agent
from crewai.tools import BaseTool
from pydantic import Field
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
from typing import List
from langchain_google_vertexai import VertexAIEmbeddings

# Load environment variables
load_dotenv()

# Fetch API keys
google_api_key = os.getenv('API_KEY')
serper_api_key = os.getenv('SERPER_API_KEY')

# Initialize Language Model (LLM)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    google_api_key=google_api_key  # Pass API key
)

# Define Agents
Router_Agent = Agent(
    role='Router',
    goal='Route user questions to a vectorstore or web search.',
    backstory=(
        "You are an expert at routing user questions to vectorstore or web search. "
        "Use vectorstore for questions about transformers or differential transformers. "
        "Use web-search for latest news or recent topics. "
        "Use generation for generic questions."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

Retriever_Agent = Agent(
    role="Retriever",
    goal="Use retrieved information to answer the question.",
    backstory=(
        "You assist in question-answering tasks. "
        "Use retrieved context to answer questions clearly and concisely."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

# Initialize Tools
search = GoogleSerperAPIWrapper(api_key=serper_api_key)

class SearchTool(BaseTool):
    name: str = "Search"
    description: str = "Useful for search-based queries about markets, companies, and trends."
    search: GoogleSerperAPIWrapper = Field(default_factory=lambda: GoogleSerperAPIWrapper(api_key=serper_api_key))

    def _run(self, query: str) -> str:
        """Execute the search query and return results."""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"

class GenerationTool(BaseTool):
    name: str = "Generation_tool"
    description: str = "Useful for generic queries based on prior knowledge."

    def _run(self, query: str) -> str:
        """Generate a response based on prior knowledge."""
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            google_api_key=google_api_key  # Ensure API key is passed
        )
        return llm.invoke(query)

# Initialize Tools
generation_tool = GenerationTool()
web_search_tool = SearchTool()

# PDF Search Tool
pdf_search_tool = PDFSearchTool(
    #pdf=r"C:\Users\PMLS\PycharmProjects\Complete-Generative-AI-\10 LLM Projects\03 Rag Multimodal\01 Agentic Rag\2410.05258v1.pdf",
    #embeddings = VertexAIEmbeddings(model="text-embedding-004")
    "This is testing"
)

# Tasks

router_task = Task(
    description=("Analyse the keywords in the question {question}"
    "Based on the keywords decide whether it is eligible for a vectorstore search or a web search or generation."
    "Return a single word 'vectorstore' if it is eligible for vectorstore search."
    "Return a single word 'websearch' if it is eligible for web search."
    "Return a single word 'generate' if it is eligible for generation."
    "Do not provide any other premable or explaination."
    ),
    expected_output=("Give a  choice 'websearch' or 'vectorstore' or 'generate' based on the question"
    "Do not provide any other premable or explaination."),
    agent=Router_Agent,
   )

retriever_task = Task(
    description=("Based on the response from the router task extract information for the question {question} with the help of the respective tool."
    "Use the web_serach_tool to retrieve information from the web in case the router task output is 'websearch'."
    "Use the rag_tool to retrieve information from the vectorstore in case the router task output is 'vectorstore'."
    "otherwise generate the output basedob your own knowledge in case the router task output is 'generate"
    ),
    expected_output=("You should analyse the output of the 'router_task'"
    "If the response is 'websearch' then use the web_search_tool to retrieve information from the web."
    "If the response is 'vectorstore' then use the rag_tool to retrieve information from the vectorstore."
    "If the response is 'generate' then use then use generation_tool ."
    "otherwise say i dont know if you dont know the answer"

    "Return a claer and consise text as response."),
    agent=Retriever_Agent,
    context=[router_task],
    tools=[pdf_search_tool,web_search_tool,generation_tool],
)
# Crew with Agents and Tasks
rag_crew = Crew(
    agents=[Router_Agent, Retriever_Agent],
    tasks=[router_task, retriever_task],
    verbose=True,
)

result = rag_crew.kickoff(inputs={"question":"What is diffrential transformer?"})

import phi
from phi.agent import Agent, RunResponse
from phi.model.google import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

import os
from dotenv import load_dotenv
load_dotenv()

#api_key = os.getenv('API_KEY')

#Configure Gemini API
#genai.configure(api_key=api_key)
#model = genai.GenerativeModel('gemini-pro')

# Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Gemini(
        id="gemini-1.5-flash"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources."],
    show_tool_calls=True,
    markdown=True,
    api_key = "xyz",


)

# Financial Agent
finance_agent = Agent(
    name="Finance AI Agent",
    model=Gemini(
        id="gemini-1.5-flash"),

        tools=[
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                stock_fundamentals=True,
                company_news=True
            )
        ],
        instructions=["Use tables to display the data."],
        show_tool_calls=True,
        markdown=True,
        api_key = "zyz",
    )

# Multi-Agent System
multi_ai_agent = Agent(
    team=[web_search_agent, finance_agent],
    model=Gemini(id="gemini-1.5-flash"),
    instructions=["Always include sources.", "Use tables to display data."],
    show_tool_calls=True,
    markdown=True,
    api_key = "xyz",
)

# Query the Multi-Agent
multi_ai_agent.print_response(
    "Summarize analyst recommendations and share the latest news for NVDA."
)

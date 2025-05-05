import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


async def main():
    agent_web = Agent(
        name="WebDevelopment",
        instructions="You are a web development expert specializing in modern frontend and backend technologies. You can provide guidance on HTML, CSS, JavaScript, React, Angular, Vue, Node.js, Express, Django, Flask, and other web frameworks. You help with code examples, best practices, architecture decisions, and troubleshooting web application issues.",
        model=model
    )

     # Mobile Development Agent
    agent_mobile = Agent(
        name="MobileDevelopment",
        instructions="You are a mobile development expert specializing in iOS and Android app development. You can provide guidance on Swift, Objective-C, Kotlin, Java, React Native, Flutter, and other mobile frameworks. You help with code examples, mobile UI/UX best practices, app architecture, performance optimization, and troubleshooting mobile application issues.",
        model=model
    )

    # DevOps Agent
    agent_devops = Agent(
        name="DevOps",
        instructions="You are a DevOps expert specializing in CI/CD pipelines, infrastructure as code, containerization, and cloud platforms. You can provide guidance on Docker, Kubernetes, Jenkins, GitHub Actions, AWS, Azure, GCP, Terraform, Ansible, and monitoring tools. You help with deployment strategies, infrastructure optimization, security best practices, and automating development workflows.",
        model=model
    )
    
    # OpenAI Agent
    agent_openai = Agent(
        name="OpenAIAgent",
        instructions="You are an OpenAI integration specialist with deep knowledge of OpenAI's APIs, models, and best practices. You can provide guidance on implementing GPT models, fine-tuning, prompt engineering, embeddings, DALL-E, and other OpenAI technologies. You help with API usage, token optimization, cost management, and building AI-powered applications using OpenAI's ecosystem.",
        model=model 
    )
    agent_agentic_ai = Agent(
        name="AgenticAI",
        instructions="""You are an AI specialist focusing on agentic systems and advanced AI implementations. 
        You understand how to build complex AI systems that can act autonomously and make decisions.
        You have access to specialized tools for DevOps and OpenAI integration.
        
        When faced with DevOps questions about CI/CD, Docker, Kubernetes, cloud platforms, or infrastructure, 
        use the devops_expert tool to get specialized answers.
        
        When faced with questions about OpenAI technologies, APIs, models, prompt engineering, or AI application development,
        use the openai_expert tool to get specialized answers.
        
        For general AI questions, answer directly using your own knowledge.""",
        model=model,
        tools=[agent_devops.as_tool(
            tool_name="devops_expert",
            tool_description="Useful for answering DevOps questions about CI/CD, Docker, Kubernetes, cloud platforms, and infrastructure."
        ), agent_openai.as_tool(
            tool_name="openai_expert",
            tool_description="Useful for answering questions about OpenAI technologies, APIs, models, prompt engineering, and AI application development."
        )
      ],
    )
    agent_panaversity = Agent(
        name="Panaversity",
        instructions="""You are Panaversity, a master coordinator for technology education and implementation.
        You have expertise across multiple domains and can delegate to specialized agents when needed.
        
        You have access to three specialized tools:
        
        1. When faced with web development questions about HTML, CSS, JavaScript, frontend frameworks, 
           backend technologies, or web application architecture, use the web_development_expert tool.
        
        2. When faced with mobile development questions about iOS, Android, React Native, Flutter, 
           mobile UI/UX, or app performance, use the mobile_development_expert tool.
        
        3. When faced with AI or DevOps questions about agent systems, OpenAI technologies, 
           CI/CD, containerization, or cloud platforms, use the agentic_ai_expert tool.
        
        For general technology questions or questions that span multiple domains, 
        you can either answer directly or use the most appropriate tool.
        
        Your goal is to provide comprehensive, accurate answers by leveraging the right expertise.""",
        model=model,
        tools=[agent_web.as_tool(
            tool_name="web_development_expert",
            tool_description="Useful for answering web development questions about HTML, CSS, JavaScript, frontend frameworks, backend technologies, and web application architecture."
        ), agent_mobile.as_tool(
            tool_name="mobile_development_expert",
            tool_description="Useful for answering mobile development questions about iOS, Android, React Native, Flutter, mobile UI/UX, and app performance."
        ), agent_agentic_ai.as_tool(
            tool_name="agantic_ai_expert",
            tool_description="Useful for answering AI or DevOps questions about agent systems, OpenAI technologies, CI/CD, containerization, and cloud platforms."
        )]
    )


    print("\n=== Testing Panaversity Agent ===\n")
    
    # Test with a web development question
    print("Web Development Question:")
    web_question = "What's the best approach for creating a responsive web application with React?"
    panaversity_result = await Runner.run(agent_panaversity, web_question, run_config=config)
    print(panaversity_result.final_output)
    print("\n" + "-"*50 + "\n")
    
    # Test with a mobile development question
    print("Mobile Development Question:")
    mobile_question = "How should I structure a Flutter app for both iOS and Android?"
    panaversity_result = await Runner.run(agent_panaversity, mobile_question, run_config=config)
    print(panaversity_result.final_output)
    print("\n" + "-"*50 + "\n")
    
    # Test with an AI/DevOps question
    print("AI/DevOps Question:")
    ai_question = "How can I deploy an OpenAI-powered application using Docker and Kubernetes?"
    panaversity_result = await Runner.run(agent_panaversity, ai_question, run_config=config)
    print(panaversity_result.final_output)
    print("\n" + "-"*50 + "\n")
    
    # Test with a cross-domain question
    print("Cross-Domain Question:")
    cross_question = "What's the best way to build a full-stack application with a React frontend, Node.js backend, and AI features using OpenAI's API?"
    panaversity_result = await Runner.run(agent_panaversity, cross_question, run_config=config)
    print(panaversity_result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
    
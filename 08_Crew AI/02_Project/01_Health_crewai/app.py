import asyncio
import os
import logging
from dotenv import load_dotenv
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Access the API keys
google_api_key = os.getenv('GOOGLE_API_KEY')
serper_api_key = os.getenv("SERPER_API_KEY")

# Ensure an event loop is available in the current thread
def ensure_event_loop():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

ensure_event_loop()

# Assign tool
serper_tool = SerperDevTool(api_key=serper_api_key)

# Use the API key in your ChatGoogleGenerativeAI instantiation
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.7,  # Adjusted temperature
    google_api_key=google_api_key
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_crewai_setup(age, gender, disease):
    # Define Agents
    fitness_expert = Agent(
        role="Fitness Expert",
        goal=f"""Analyze the fitness requirements for a {age}-year-old {gender} with {disease} and 
                 suggest exercise routines and fitness strategies""",
        backstory=f"""Expert at understanding fitness needs, age-specific requirements, 
                      and gender-specific considerations. Skilled in developing 
                      customized exercise routines and fitness strategies.""",
        verbose=True,
        llm=llm,
        allow_delegation=True,
        tools=[serper_tool],
    )
    
    nutritionist = Agent(
        role="Nutritionist",
        goal=f"""Assess nutritional requirements for a {age}-year-old {gender} with {disease} and 
                 provide dietary recommendations""",
        backstory=f"""Knowledgeable in nutrition for different age groups and genders, 
                      especially for individuals of {age} years old. Provides tailored 
                      dietary advice based on specific nutritional needs.""",
        verbose=True,
        llm=llm,
        allow_delegation=True,
    )
    
    doctor = Agent(
        role="Doctor",
        goal=f"""Evaluate the overall health considerations for a {age}-year-old {gender} with {disease} and 
                 provide recommendations for a healthy lifestyle. Pass it on to the
                  disease_expert if you are not an expert of {disease}.""",
        backstory=f"""Medical professional experienced in assessing overall health and 
                      well-being. Offers recommendations for a healthy lifestyle 
                      considering age, gender, and disease factors.""",
        verbose=True,
        llm=llm,
        allow_delegation=True,
    )

    task1 = Task(
        description=f"""Analyze the fitness requirements for a {age}-year-old {gender} with {disease}. 
                        Provide recommendations for exercise routines and fitness strategies.""",
        agent=fitness_expert,
        llm=llm,
        expected_output="Fitness recommendations and strategies"
    )

    task2 = Task(
        description=f"""Assess nutritional requirements for a {age}-year-old {gender} with {disease}. 
                        Provide dietary recommendations based on specific nutritional needs.""",
        agent=nutritionist,
        llm=llm,
        expected_output="Dietary recommendations"
    )

    task3 = Task(
        description=f"""Evaluate overall health considerations for a {age}-year-old {gender} with {disease}. 
                        Provide recommendations for a healthy lifestyle.""",
        agent=doctor,
        llm=llm,
        expected_output="Health and lifestyle recommendations"
    )

    if disease.lower() != "none":
        disease_expert = Agent(
            role="Disease Expert",
            goal=f"""Provide recommendations for managing {disease}""",
            backstory=f"""Specialized in dealing with individuals having {disease}. 
                          Offers tailored advice for managing the specific health condition.""",
            verbose=True,
            llm=llm,
            allow_delegation=True,
        )
        disease_task = Task(
            description=f"""Provide recommendations for managing {disease}""",
            agent=disease_expert,
            llm=llm,
            expected_output="Disease management recommendations"
        )
        health_crew = Crew(
            agents=[fitness_expert, 
                    nutritionist, doctor, disease_expert],
            tasks=[task1, task2, task3, disease_task],
            verbose=2,
            process=Process.sequential,
        )
    else:
        health_crew = Crew(
            agents=[fitness_expert, nutritionist, doctor],
            tasks=[task1, task2, task3],
            verbose=2,
            process=Process.sequential,
        )

    # Start the process and log results
    try:
        crew_result = health_crew.kickoff()
        logger.info(f"Crew process completed with result: {crew_result}")
        return crew_result
    except Exception as e:
        logger.error(f"Error during crew process: {e}")
        return str(e)


# Streamlit Interface
def main():
    st.title("🏥 Health CrewAI ")



    # Specify the image path
    image_path = "C:\\Users\\PMLS\Desktop\\02_Project\\AI ASSIS.jpeg"

    # Open the original image
    original_image = Image.open(image_path)

    # Resize the image to your desired dimensions (e.g., 600x400 pixels)
    resized_image = original_image.resize((600, 400), Image.ANTIALIAS)

    # Display the resized image
    st.image(resized_image, caption="Health CrewAI", use_column_width=True)



    st.markdown("""
    Welcome to the **Health CrewAI Setup**! 🚀
    
    Please provide the following details to get personalized health recommendations:
    """)

    age = st.number_input("Enter age:", min_value=0, value=30)
    gender = st.selectbox("Select gender:", ["male", "female", "other"])
    disease = st.text_input("Enter disease (or 'none' if no disease):", value="none")

    if st.button("Submit"):
        with st.spinner("Processing... ⏳"):
            result = create_crewai_setup(age, gender, disease)
            st.success("Process completed! ✅")
            st.write("Results:")
            st.write(result)

if __name__ == "__main__":
    main()
This is a simple web application that allows users to query a language model by entering a question in a text input field. The prompt, language model, and output parser are defined using the langchain_openai, langchain_core, and langchain_community libraries, and the web application is built using the streamlit library.

Setup
To run this application, you will need to have Python 3.6 or higher installed. You will also need to install the required libraries by running the following command:

Copy code
pip install -r requirements.txt
Additionally, you will need to create a .env file in the root directory of the project with the following environment variables:

LANGCHAIN_API_KEY: Your API key for the language model.
LANGCHAIN_TRACING_V2: Set to true to enable tracing for the language model.
Usage
To run the application, simply execute the following command:

Copy code
streamlit run app.py
This will start the web application on your local machine. You can then open a web browser and navigate to http://localhost:8501 to use the application.

Code Overview
Here's a breakdown of what each part of the code does:

from langchain_openai import ChatOpenAI: Imports the ChatOpenAI class from the langchain_openai library.
from langchain_core.prompts import ChatPromptTemplate: Imports the ChatPromptTemplate class from the langchain_core library.
from langchain_core.output_parsers import StrOutputParser: Imports the StrOutputParser class from the langchain_core library.
from langchain_community.llms import Ollama: Imports the Ollama class from the langchain_community library.
import streamlit as st: Imports the streamlit library for building web applications in Python.
import os: Imports the os library for working with environment variables.
from dotenv import load_dotenv: Imports the load_dotenv function from the dotenv library for loading environment variables from a .env file.
load_dotenv(): Loads environment variables from a .env file (if it exists).
os.environ["LANGCHAIN_TRACING_V2"]="true": Sets the LANGCHAIN_TRACING_V2 environment variable to true.
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY"): Sets the LANGCHAIN_API_KEY environment variable to the value of the LANGCHAIN_API_KEY environment variable in the .env file.
prompt=ChatPromptTemplate.from_messages([("system","You are a helpful assistant. Please response to the user queries"),("user","Question:{question}")]): Creates a ChatPromptTemplate object, which defines the prompt that will be used to query the language model. The prompt consists of two messages: one from the "system" (i.e., the application) and one from the "user". The user message includes a placeholder for the user's question.
st.title('Model locally'): Sets the title of the web application.
input_text=st.text_input("Search the topic u want"): Creates a text input field for the user to enter their question.
llm=Ollama(model="phi3"): Creates an Ollama object, which represents the language model. The model is specified by the model parameter (in this case, "phi3").
output_parser=StrOutputParser(): Creates a StrOutputParser object, which will be used to parse the output of the language model.
chain=prompt|llm|output_parser: Creates a chain object by chaining together the prompt, language model, and output parser.
if input_text: st.write(chain.invoke({"question":input_text})): Checks if the user has entered a question in the text input field. If they have, it invokes the chain object with the user's question and writes the output to the web application.
License

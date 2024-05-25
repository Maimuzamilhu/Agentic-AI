from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn 
import os
from langchain_community.llms import Ollama 
from dotenv import load_dotenv
 
load_dotenv()





app = FastAPI(
    title="LAngchain Server",
    version= "1.0",
    description= "A Simple API Server  "
)




# ollama phi3
llm = Ollama(model = "phi3")

prompt1 = ChatPromptTemplate.from_template("Write me an essy about {topic} with 100 words")
prompt2 = ChatPromptTemplate.from_template("Write me an poen about {topic} with 100 words")


add_routes(
    app,
    prompt1|llm,
    path="/essay"
)
add_routes(
    app,
    prompt2|llm,
    path="/poem"
)

if __name__ =="__main__":
    uvicorn.run(app , host="localhost" , port=8000)
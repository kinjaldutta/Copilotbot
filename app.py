from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os

# Import langchain components
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Langchain API is running"}

@app.post("/ask")
async def process_question(request: Request):
    data = await request.json()
    question = data.get("query", "")
    
    # Initialize the language model
    llm = ChatOpenAI(temperature=0.7)
    
    # Create a prompt template
    template = """
    You are a helpful assistant that provides informative responses.
    
    Question: {question}
    
    Answer:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["question"])
    
    # Create and run the chain
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(question=question)
    
    return {"response": response}

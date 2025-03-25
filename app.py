# app.py (updated to use .env file)
from flask import Flask, request, jsonify
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Create a simple Langchain prompt template
template = """Question: {question}

Answer: """
prompt = PromptTemplate(template=template, input_variables=["question"])

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    if not data or 'question' not in data:
        return jsonify({"error": "Please provide a question"}), 400
    
    # Get the question from the request
    question = data['question']
    
    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        return jsonify({"error": "OpenAI API key not found in environment variables"}), 500
    
    # Use the newer pattern with pipe operator
    llm = OpenAI(temperature=0.7)
    chain = prompt | llm
    
    # Run the chain
    response = chain.invoke({"question": question})
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

# app.py (with Render.com port configuration)
from flask import Flask, request, jsonify
from langchain.llms import OpenAI
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

@app.route('/', methods=['GET'])
def home():
    return "Langchain API is running! Send POST requests to /ask"

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
    
    # Initialize OpenAI LLM and run the prompt
    try:
        llm = OpenAI(temperature=0.7)
        response = llm(prompt.format(question=question))
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

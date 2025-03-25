# app.py
from flask import Flask, request, jsonify
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

app = Flask(__name__)

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"

# Create a simple Langchain prompt template
template = """Question: {question}

Answer: """
prompt = PromptTemplate(template=template, input_variables=["question"])

# Create a Langchain chain
llm = OpenAI(temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    if not data or 'question' not in data:
        return jsonify({"error": "Please provide a question"}), 400
    
    # Get the question from the request
    question = data['question']
    
    # Run the chain
    response = chain.run(question)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Set OpenAI API Key (Store in Render ENV Variables)
import os
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Function to interact with Vakil GPT
def chat_with_vakil_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Vakil GPT, an AI specializing in Indian legal guidance."},
            {"role": "user", "content": message}
        ]
    )
    return response["choices"][0]["message"]["content"]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")

    try:
        reply = chat_with_vakil_gpt(user_message)
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Change port for Render

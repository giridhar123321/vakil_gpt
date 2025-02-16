from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Set OpenAI API Key (from Render Environment Variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Use new client format

# Function to interact with Vakil GPT
def chat_with_vakil_gpt(message):
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Vakil GPT, an AI specializing in Indian legal guidance."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content  # Updated format

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
    app.run(host='0.0.0.0', port=10000)

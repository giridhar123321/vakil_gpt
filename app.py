import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to interact with Gemini AI
def chat_with_vakil_gpt(message):
    try:
        model = genai.GenerativeModel("gemini-pro")  # Free Gemini model
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# API route for chatbot
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

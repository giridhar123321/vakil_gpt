import os
import google.generativeai as genai
from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests
app.secret_key = "supersecretkey"  # Required for session management

# Load Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to interact with Gemini AI for Indian legal assistance
def chat_with_vakil_gpt(user_message):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # Updated to Gemini 2.0 Flash

        # Retrieve session history or initialize it
        if "chat_history" not in session:
            session["chat_history"] = []
        
        # Append new user message to chat history
        session["chat_history"].append({"role": "user", "parts": [{"text": user_message}]})

        # Generate response from Gemini
        response = model.generate_content(session["chat_history"])
        
        # Store the assistant's response in session history
        session["chat_history"].append({"role": "assistant", "parts": [{"text": response.text}]})

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

# API route to clear session memory
@app.route('/clear_session', methods=['POST'])
def clear_session():
    session.pop("chat_history", None)
    return jsonify({"message": "Session history cleared."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

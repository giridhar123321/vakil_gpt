import os
import google.generativeai as genai
from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests
app.secret_key = "supersecretkey"  # Required for session storage

# Load Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# System prompt for Vakil GPT (Legal Assistant for Indian Law)
SYSTEM_PROMPT = """
VakilMate – Your AI Legal Research Assistant for Indian Law
VakilMate is an AI-powered legal assistant specializing in Indian law, designed to provide general legal information and assist in legal research for both lawyers and non-lawyers.

Scope of Legal Information Covered:
1️⃣ Criminal Law - IPC, CrPC, NDPS Act, etc.
2️⃣ Property Law - TOPA, RERA, Land & Tenancy Laws.
3️⃣ Contract Law - Indian Contract Act, Special Contracts.
4️⃣ Family Law - Marriage, Divorce, Succession.
5️⃣ Consumer Protection Law - Consumer Protection Act, E-commerce regulations.
6️⃣ Cyber Law & Data Protection - IT Act, Online Defamation.

Rules for Responses:
🔹 No Personal Legal Advice - General information only.
🔹 Simplified Legal Explanations for non-lawyers.
🔹 Research-Oriented Approach for legal professionals with case laws and statutory references.
🔹 Transparency on Uncertainty - Recommend legal consultation when required.
🔹 Jurisdiction-Specific - Focused on Indian law with state variations where applicable.
"""

# Function to interact with Gemini AI for legal assistance
def chat_with_vakil_gpt(user_message):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # Ensure correct model is used

        # Retrieve chat history from session
        chat_history = session.get("chat_history", [])

        # Add system prompt if it's a new session
        if not chat_history:
            chat_history.append({"role": "system", "parts": [{"text": SYSTEM_PROMPT}]})

        # Append new user message
        chat_history.append({"role": "user", "parts": [{"text": user_message}]})

        # Ensure full chat history is passed
        response = model.generate_content(chat_history)

        # Store assistant's response in chat history
        chat_history.append({"role": "assistant", "parts": [{"text": response.text}]})

        # Save updated session history
        session["chat_history"] = chat_history
        session.modified = True  # Ensure session changes are saved

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

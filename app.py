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

# Function to interact with Gemini AI with Indian legal specialization
def chat_with_vakil_gpt(message):
    try:
        model = genai.GenerativeModel("gemini-pro")  # Free Gemini model
        
        system_prompt = """ 
        You are Vakil GPT, an AI legal assistant specializing in Indian law. 
        Your job is to provide **general legal information** on:
        - Indian **criminal law** (IPC, CrPC)
        - **Property law** (transfer of property, RERA)
        - **Contract law** (Indian Contract Act, agreements)
        - **Family law** (marriage, divorce, inheritance)
        - **Consumer rights** (Consumer Protection Act)
        - **Cyber law** (IT Act)

        **Rules for response:**
        1️⃣ **DO NOT give personal legal advice.** Instead, suggest consulting a lawyer.
        2️⃣ Use **simple, understandable language** for non-lawyers.
        3️⃣ If you don't know the answer, say **"I recommend consulting a legal expert."**
        """

        response = model.generate_content(
            [
                {"parts": [{"text": system_prompt}]}, 
                {"parts": [{"text": message}]}
            ]
        )

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

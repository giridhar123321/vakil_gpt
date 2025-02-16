from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Set your OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key_here"
openai.api_key = OPENAI_API_KEY

# Function to communicate with Vakil GPT
def chat_with_vakil_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # GPT-4 (Vakil GPT is a custom instruction-based model)
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
    app.run(debug=True)

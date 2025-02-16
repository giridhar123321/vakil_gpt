import os
import deepseek

# Load API key from environment variables
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def chat_with_vakil_gpt(message):
    try:
        client = deepseek.ChatClient(api_key=DEEPSEEK_API_KEY)
        response = client.chat(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are Vakil GPT, an AI specializing in Indian legal guidance."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except deepseek.DeepSeekError as e:
        return f"⚠️ Error: {str(e)}"

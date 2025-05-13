import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the chat session
chat = genai.GenerativeModel(GEMINI_MODEL).start_chat(history=[])

def get_response(prompt):
    """Get response from the AI model"""
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        print(f"AI error: {e}")
        return "I'm having trouble connecting to my AI service. Please try again."
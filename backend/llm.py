import os
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env
load_dotenv()

class llmChatService:
    def __init__(self):
        # Configure Gemini with your API key
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')

    async def get_chat_response(self, user_message: str, chat_history: list) -> str:

        try:
            formatted_history = []
            for msg in chat_history:
                if isinstance(msg.parts, list) and all(isinstance(p, str) for p in msg.parts):
                    formatted_parts = [{"text": p} for p in msg.parts]
                else:
                    formatted_parts = msg.parts 

                formatted_history.append({
                    "role": msg.role,
                    "parts": formatted_parts
                })

            # Start a chat session
            chat_session = self.model.start_chat(history=formatted_history)

            # Send the current user message
            # `send_message_async` expects the current message as a string directly
            response = await chat_session.send_message_async(user_message)

            # Extract the response text
            return response.text

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            raise
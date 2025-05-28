import os
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env
load_dotenv()

class llmChatService:
    def __init__(self):
        # Configure Gemini with your API key
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')

    async def get_chat_response(self, user_message: str, chat_history: list) -> str:

        try:
            # Define the system instruction for the Travel Buddy persona
            system_instruction_message = {
                "role": "user", # The instruction is given as if from the user
                "parts": [{"text": (
                    "You are a helpful and friendly travel planning assistant named 'Travel Buddy'. "
                    "Your primary goal is to assist users with travel-related queries, "
                    "including destinations, planning itineraries, packing, booking tips, local customs, "
                    "and general travel advice. "
                    "If a user asks a question not related to travel, gently remind them that "
                    "you are a travel assistant and can only help with travel-specific topics."
                )}]
            }

            formatted_history = [system_instruction_message]
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
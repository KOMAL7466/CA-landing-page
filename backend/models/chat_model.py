import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class ChatModel:
    def __init__(self):
        """Initialize Gemini model for chat"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found")
            self.model = None
            return
        
        genai.configure(api_key=self.api_key)
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
            logger.info("Chat model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize chat model: {e}")
            self.model = None
    
    async def get_response(self, message: str) -> str:
        """Get response from Gemini"""
        if not self.model:
            return "AI model not initialized. Please check API key."
        
        try:
            prompt = f"""You are a professional Chartered Accountant assistant. 
            Answer the following question in a helpful, accurate manner:
            
            Question: {message}
            
            Provide clear, concise information about accounting, tax, or finance.
            If not CA-related, politely redirect.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return f"Error: {str(e)}"
import os
import shutil
import google.generativeai as genai
from dotenv import load_dotenv
import logging
from utils.text_extractor import extract_text_from_file
from utils.classifier import is_ca_related
from datetime import datetime, timedelta

load_dotenv()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadModel:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
            self.quota_reset_time = None
        else:
            self.model = None
    
    async def process_file(self, file):
        """Process uploaded file with user-friendly messages"""
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        content = await file.read()
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Check quota cooldown
        if self.quota_reset_time and datetime.now() < self.quota_reset_time:
            return {
                "status": "quota_error",
                "is_ca_related": False,
                "analysis": None,
                "message": "⏳ **Daily Analysis Limit Reached**\n\nThe document analysis feature has reached its daily limit. This resets automatically every 24 hours.\n\n✨ **Demo Note:** This shows our error handling. In production, upgrade to paid tier for unlimited analysis.",
                "text_preview": "",
                "quota_reset": self.quota_reset_time.isoformat()
            }
        
        extracted_text = extract_text_from_file(file_path, file.content_type)
        is_ca = is_ca_related(extracted_text)
        
        # Analyze with Gemini
        analysis = self.analyze_document(extracted_text) if self.model else "Analysis unavailable"
        
        # Check if analysis contains quota error
        if analysis and "quota" in analysis.lower() and "429" in analysis:
            # Parse retry time
            import re
            retry_match = re.search(r'retry[_\s]?delay[_\s]?[:\s]+(\d+)', analysis.lower())
            if retry_match:
                retry_seconds = int(retry_match.group(1))
                self.quota_reset_time = datetime.now() + timedelta(seconds=retry_seconds)
            
            return {
                "status": "quota_error",
                "is_ca_related": is_ca,
                "analysis": "📊 **Analysis Temporarily Unavailable**\n\nThe AI analysis feature has reached its rate limit. Please wait a few minutes and try again.\n\n💡 **This is a free tier limitation.** In production, paid plans offer unlimited analysis.",
                "text_preview": extracted_text[:200],
                "quota_reset": self.quota_reset_time.isoformat() if self.quota_reset_time else None
            }
        
        return {
            "status": "success",
            "is_ca_related": is_ca,
            "analysis": analysis,
            "text_preview": extracted_text[:200]
        }
    
    def analyze_document(self, text: str) -> str:
        """Analyze document with Gemini"""
        if not self.model:
            return "Analysis service unavailable"
        
        try:
            prompt = f"""Analyze this financial document and provide key insights:
            
            {text[:2000]}
            
            Provide brief summary and important points."""
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return f"Analysis temporarily unavailable. Please try again."
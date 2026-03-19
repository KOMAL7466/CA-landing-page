import os
import shutil
import google.generativeai as genai
from dotenv import load_dotenv
import logging
from utils.text_extractor import extract_text_from_file
from utils.classifier import is_ca_related

load_dotenv()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadModel:
    def __init__(self):
        """Initialize models for upload processing"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        else:
            self.model = None
    
    async def process_file(self, file):
        """Process uploaded file"""
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        content = await file.read()
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Extract text
        extracted_text = extract_text_from_file(file_path, file.content_type)
        
        # Check if CA-related
        is_ca = is_ca_related(extracted_text)
        
        # Analyze with Gemini
        analysis = self.analyze_document(extracted_text) if self.model else "Analysis unavailable"
        
        return {
            "is_ca_related": is_ca,
            "analysis": analysis,
            "text_preview": extracted_text[:200]
        }
    
    def analyze_document(self, text: str) -> str:
        """Analyze document with Gemini"""
        try:
            prompt = f"""Analyze this financial document and provide key insights:
            
            {text[:2000]}
            
            Provide brief summary and important points."""
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return "Analysis failed"
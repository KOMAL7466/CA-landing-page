import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging
from datetime import datetime
from utils.text_extractor import extract_text_from_file
from utils.classifier import is_ca_related

load_dotenv()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class AuditModel:
    def __init__(self):
        """Initialize audit model"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        else:
            self.model = None
    
    async def perform_audit(self, file, query: str, year: str):
        """Perform audit on document"""
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        content = await file.read()
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Extract text
        extracted_text = extract_text_from_file(file_path, file.content_type)
        
        if not extracted_text or len(extracted_text.strip()) < 50:
            return {
                "status": "error",
                "message": "Could not extract sufficient text from document"
            }
        
        # Check if CA-related
        if not is_ca_related(extracted_text):
            return {
                "status": "error",
                "message": "Document not CA-related"
            }
        
        # Perform audit with Gemini
        audit_report = self.generate_audit_report(extracted_text, query, year)
        
        return {
            "status": "success",
            "audit_report": audit_report,
            "document_name": file.filename,
            "audit_date": datetime.now().isoformat()
        }
    
    def generate_audit_report(self, text: str, query: str, year: str) -> str:
        """Generate audit report using Gemini"""
        if not self.model:
            return "Audit model not initialized"
        
        try:
            prompt = f"""
            You are a professional Chartered Accountant. Perform a detailed audit.
            
            Financial Year: {year}
            User Query: {query}
            
            Document Content:
            {text[:5000]}
            
            Provide:
            1. Document Summary
            2. Key Findings (Top 5)
            3. Audit Methodology
            4. Recommendations
            5. Confidence Score (0-100%)
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Audit generation error: {e}")
            return f"Audit failed: {str(e)}"
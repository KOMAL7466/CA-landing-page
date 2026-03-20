import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
from utils.text_extractor import extract_text_from_file
from utils.classifier import is_ca_related

load_dotenv()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class AuditModel:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
            self.quota_reset_time = None
        else:
            self.model = None
    
    async def perform_audit(self, file, query: str, year: str):
        """Perform audit on document with user-friendly messages"""
        
        # Check quota cooldown
        if self.quota_reset_time and datetime.now() < self.quota_reset_time:
            return {
                "status": "quota_error",
                "message": "⏳ **Audit Feature Temporarily Unavailable**\n\nThe AI audit feature has reached its daily limit. This resets automatically every 24 hours.\n\n**Demo Note:** This shows our quota handling. In production, upgrade to paid tier for unlimited audits.",
                "document_name": file.filename,
                "audit_date": datetime.now().isoformat()
            }
        
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        content = await file.read()
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        extracted_text = extract_text_from_file(file_path, file.content_type)
        
        if not extracted_text or len(extracted_text.strip()) < 50:
            return {
                "status": "error",
                "message": "⚠️ **Insufficient Text**\n\nCould not extract enough text from this document. Please ensure it contains readable financial data."
            }
        
        if not is_ca_related(extracted_text):
            return {
                "status": "error",
                "message": "📄 **Document Type Not Supported**\n\nThis document doesn't appear to be CA-related. Please upload financial documents like:\n• Invoices\n• Receipts\n• Balance Sheets\n• Tax Forms\n• Financial Statements"
            }
        
        audit_report = self.generate_audit_report(extracted_text, query, year)
        
        # Check if report contains quota error
        if "quota" in audit_report.lower() and "429" in audit_report:
            import re
            retry_match = re.search(r'retry[_\s]?delay[_\s]?[:\s]+(\d+)', audit_report.lower())
            if retry_match:
                retry_seconds = int(retry_match.group(1))
                self.quota_reset_time = datetime.now() + timedelta(seconds=retry_seconds)
            
            return {
                "status": "quota_error",
                "message": "📊 **Audit Queue Full**\n\nThe audit feature is temporarily busy. Please wait a few minutes and try again.\n\n💡 **Free tier limitation:** 10 audits per minute. Paid plans offer unlimited audits.",
                "document_name": file.filename,
                "audit_date": datetime.now().isoformat()
            }
        
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
            if "429" in str(e):
                return "QUOTA_ERROR: Rate limit reached"
            return f"Audit failed. Please try again."
import PIL.Image
import pdfplumber
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_text_from_file(file_path: str, content_type: str = "") -> str:
    """Extract text from various file types"""
    try:
        if content_type and content_type.startswith('image/'):
            return extract_image_text(file_path)
        elif file_path.endswith('.pdf'):
            return extract_pdf_text(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return extract_excel_text(file_path)
        elif file_path.endswith('.csv'):
            return extract_csv_text(file_path)
        else:
            return "Unsupported file type"
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        return ""

def extract_image_text(file_path):
    """Extract text from image using PIL"""
    try:
        img = PIL.Image.open(file_path)
        # For now, just return image info
        return f"Image file: {file_path}, Size: {img.size}"
    except Exception as e:
        return f"Image extraction error: {e}"

def extract_pdf_text(file_path):
    """Extract text from PDF"""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages[:3]:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text[:5000]
    except Exception as e:
        return f"PDF extraction error: {e}"

def extract_excel_text(file_path):
    """Extract text from Excel"""
    try:
        df = pd.read_excel(file_path)
        return df.to_string()[:5000]
    except Exception as e:
        return f"Excel extraction error: {e}"

def extract_csv_text(file_path):
    """Extract text from CSV"""
    try:
        df = pd.read_csv(file_path)
        return df.to_string()[:5000]
    except Exception as e:
        return f"CSV extraction error: {e}"
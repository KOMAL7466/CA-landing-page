from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import logging
from models.audit_model import AuditModel

router = APIRouter()
audit_model = AuditModel()
logger = logging.getLogger(__name__)

@router.post("/audit")
async def audit_document(
    file: UploadFile = File(...),
    query: Optional[str] = Form("Perform audit on this financial document"),
    year: Optional[str] = Form("2025-2026")
):
    """Audit endpoint for financial documents"""
    try:
        logger.info(f"Audit request: {file.filename}")
        
        result = await audit_model.perform_audit(file, query, year)
        
        return result
        
    except Exception as e:
        logger.error(f"Audit error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
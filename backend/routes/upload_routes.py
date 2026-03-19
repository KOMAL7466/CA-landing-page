from fastapi import APIRouter, UploadFile, File, HTTPException
import logging
from models.upload_model import UploadModel

router = APIRouter()
upload_model = UploadModel()
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """File upload endpoint"""
    try:
        logger.info(f"Upload request: {file.filename}")
        
        result = await upload_model.process_file(file)
        
        return {
            "status": "success",
            "filename": file.filename,
            "analysis": result
        }
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
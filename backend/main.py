from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import routers
from routes import chat_routes, upload_routes, audit_routes

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CA AI Assistant API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001",
        "https://ca-landing-page-five.vercel.app",  
        "https://ca-landing-page.vercel.app"      
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_routes.router, prefix="/api", tags=["Chat"])
app.include_router(upload_routes.router, prefix="/api", tags=["Upload"])
app.include_router(audit_routes.router, prefix="/api", tags=["Audit"])

@app.get("/")
def root():
    return {
        "message": "CA AI Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "upload": "/api/upload",
            "audit": "/api/audit",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "chat": "active",
            "upload": "active", 
            "audit": "active"
        }
    }
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# CORS – frontend ko allow karo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploaded files store karne ke liye folder
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "CA Backend is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # File save karo
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Mock analysis return karo
    return {
        "message": f"File {file.filename} uploaded successfully",
        "analysis": "This is a mock analysis. AI will analyze soon."
    }

@app.post("/chat")
async def chat(message: dict):
    user_msg = message.get("message", "")
    reply = f"AI Assistant: Aapne pucha '{user_msg}'. Main CA assistant hoon."
    return {"reply": reply}
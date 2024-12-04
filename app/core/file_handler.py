import os
import shutil
from fastapi import UploadFile
from app.config import settings

UPLOAD_DIR = "static/profile_pictures"

async def save_upload_file(file: UploadFile, username: str) -> str:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_extension = os.path.splitext(file.filename)[1]
    destination = f"{UPLOAD_DIR}/{username}{file_extension}"
    
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return f"/static/profile_pictures/{username}{file_extension}"


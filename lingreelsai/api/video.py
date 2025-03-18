from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from lingreelsai.services.video_service import process_video
from lingreelsai.db import get_db

router = APIRouter()

@router.post("/upload")
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db)):
    video_path = f"{file.filename}"

    # Save the uploaded video
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    # Process the video (NLP + Vision)
    result = process_video(video_path, db)

    return {"message": "Video processed successfully", "highlights": result}

@router.post("/process")
def process_video():
    return {"message": "Video processing started"}

@router.post("/processed")
def get_processed_videos():
    return {"message": "List of processed videos"}
from fastapi import FastAPI, UploadFile, File, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from lingreelsai.nlp.natural_language_processing import transcribe_audio
from lingreelsai.vision.computer_vision import extract_highlights
from lingreelsai.db import get_db
from lingreelsai.models.models import Clip
from lingreelsai.api.auth import router as auth_router
from lingreelsai.api.video import router as video_router

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Clip Extraction API"}

@app.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    video_type: str = Form(...), 
    db: Session = Depends(get_db)
):
    video_path = f"{file.filename}"

    # Save the uploaded video
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract audio transcription
    transcript = transcribe_audio(video_path)

    # Perform visual analysis
    highlights = extract_highlights(video_path, video_type)

    print(transcript)
    print(highlights)
    # Store in database
    # for highlight in highlights:
    #     clip = Clip(
    #         video_id=1,
    #         start_time=highlight["start"],
    #         end_time=highlight["end"],
    #         description=highlight["description"]
        # )
    #     db.add(clip)

    # db.commit()

    return {"message": "Video processed successfully", "highlights": highlights}


app.include_router(video_router, prefix="/video", tags=["video"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
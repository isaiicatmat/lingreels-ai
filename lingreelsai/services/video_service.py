from lingreelsai.nlp.natural_language_processing import transcribe_audio
from lingreelsai.vision.computer_vision import extract_highlights
from lingreelsai.models.models import Clip
from sqlalchemy.orm import Session

def process_video(video_path: str, db: Session):
    # Extract audio transcription
    transcript = transcribe_audio(video_path)

    # Perform visual analysis
    highlights = extract_highlights(video_path)

    # Store highlights in database
    for highlight in highlights:
        clip = Clip(
            video_id=1,  # Adjust this depending on the relationship between video and clips
            start_time=highlight["start"],
            end_time=highlight["end"],
            description=highlight["description"]
        )
        db.add(clip)

    db.commit()

    return highlights
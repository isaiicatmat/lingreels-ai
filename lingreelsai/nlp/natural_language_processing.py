import whisper

def transcribe_audio(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)

    # Extract timestamps
    segments = []
    for segment in result['segments']:
        segments.append({
            "start": segment['start'],
            "end": segment['end'],
            "text": segment['text']
        })
    return segments
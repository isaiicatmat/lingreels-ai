import cv2
import numpy as np
import mediapipe as mp
import librosa
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def select_video_type():
    """Display a dialog to select the video type."""
    options = ["General Purpose", "Sports/Action", "Interviews/Conferences", "Movies/Shows", "Social Media"]
    selected_type = simpledialog.askstring("Select Video Type", f"Choose the video type:\n{', '.join(options)}")
    return selected_type

def extract_highlights(video_path, video_type):
    """Extract highlights based on the selected video type."""
    
    cap = cv2.VideoCapture(video_path)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / frame_rate
    
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.6)
    
    highlights = []
    frame_count = 0
    highlight_start = None
    last_scene_change = 0
    motion_threshold = 500
    prev_frame = None

    # Load audio for analysis
    y, sr = librosa.load(video_path, sr=None)

    def add_highlight(start, end, desc):
        """Add a highlight clip to the list."""
        highlights.append({
            "start": start,
            "end": end,
            "description": desc
        })

    print(f"Processing {video_type}...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        current_time = frame_count / frame_rate

        # Convert frame for face detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 🔥 General Purpose (Multi-Criteria)
        if video_type == "General Purpose":
            # 🎯 Face Detection
            results = face_detection.process(rgb_frame)
            if results.detections:
                if highlight_start is None:
                    highlight_start = current_time
            else:
                if highlight_start is not None:
                    add_highlight(highlight_start, current_time, "Detected face movement")
                    highlight_start = None

            # 🔥 Scene Change Detection
            if prev_frame is not None:
                diff = cv2.absdiff(frame, prev_frame)
                motion = np.sum(diff)
                if motion > motion_threshold and current_time - last_scene_change > 3:
                    add_highlight(current_time, current_time + 5, "Scene change")
                    last_scene_change = current_time

            prev_frame = frame.copy()

        # ⚽ Sports/Action (Motion + Audio)
        elif video_type == "Sports/Action":
            if prev_frame is not None:
                diff = cv2.absdiff(frame, prev_frame)
                motion = np.sum(diff)
                if motion > motion_threshold:
                    add_highlight(current_time, current_time + 5, "Fast movement detected")

            # 🎵 Audio Peaks
            audio_section = y[int(current_time * sr):int((current_time + 1) * sr)]
            rms = librosa.feature.rms(y=audio_section).mean()
            if rms > 0.1:  # Detect loud sections
                add_highlight(current_time, current_time + 5, "Loud audio spike")

            prev_frame = frame.copy()

        # 🎤 Interviews/Conferences (Face + Audio)
        elif video_type == "Interviews/Conferences":
            # 🎯 Face Detection
            results = face_detection.process(rgb_frame)
            if results.detections:
                if highlight_start is None:
                    highlight_start = current_time
            else:
                if highlight_start is not None:
                    add_highlight(highlight_start, current_time, "Speaker detected")
                    highlight_start = None

            # 🎵 Audio Detection
            audio_section = y[int(current_time * sr):int((current_time + 1) * sr)]
            rms = librosa.feature.rms(y=audio_section).mean()
            if rms > 0.05:  # Detect speaking
                add_highlight(current_time, current_time + 5, "Speech detected")

        # 🎬 Movies/Shows (Scene + Face)
        elif video_type == "Movies/Shows":
            if prev_frame is not None:
                diff = cv2.absdiff(frame, prev_frame)
                motion = np.sum(diff)
                if motion > motion_threshold and current_time - last_scene_change > 5:
                    add_highlight(current_time, current_time + 5, "Scene transition")
                    last_scene_change = current_time

            # 🎯 Face Detection
            results = face_detection.process(rgb_frame)
            if results.detections:
                add_highlight(current_time, current_time + 5, "Face detected")

            prev_frame = frame.copy()

        # 📱 Social Media (Short + Dynamic)
        elif video_type == "Social Media":
            # 🎯 Face Detection
            results = face_detection.process(rgb_frame)
            if results.detections:
                add_highlight(current_time, current_time + 5, "Face detected")

            # 🎵 Audio Spikes
            audio_section = y[int(current_time * sr):int((current_time + 1) * sr)]
            rms = librosa.feature.rms(y=audio_section).mean()
            if rms > 0.08:
                add_highlight(current_time, current_time + 5, "Loud audio detected")

            # ⏱️ Short Interval Highlights
            if frame_count % (frame_rate * 10) == 0:
                add_highlight(current_time, current_time + 5, "Short interval highlight")

    cap.release()
    
    # Display the extracted highlights
    for h in highlights:
        print(f"{h['description']}: {h['start']}s → {h['end']}s")

    return highlights

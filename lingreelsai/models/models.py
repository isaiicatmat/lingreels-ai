from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import enum

Base = declarative_base()

class ClipLengthEnum(enum.Enum):
    SHORT = "SHORT"
    MEDIUM = "MEDIUM"
    LONG = "LONG"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # Only if using local auth
    role = Column(String(50), default='user')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    video_url = Column(String(255), nullable=False)
    video_length = Column(Float)
    file_path = Column(String)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User")
    clips = relationship("Clip", back_populates="video")

class Clip(Base):
    __tablename__ = 'clips'

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    start_time = Column(Float)  # Start time in seconds
    end_time = Column(Float)    # End time in seconds
    clip_url = Column(String(255))
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    virality_score = Column(Float, nullable=True)
    thumbnail = Column(String, nullable=True)
    preferred_clip_length = Column(Enum(ClipLengthEnum, name='cliplengthenum', native_enum=False), nullable=True)

    video = relationship("Video", back_populates="clips")
    text_overlays = relationship("TextOverlay", back_populates="clip")
    transitions = relationship("Transition", back_populates="clip")
    music_tracks = relationship("MusicTrack", back_populates="clip")
    captions = relationship("Caption", back_populates="clip")
    emoji_overlays = relationship("EmojiOverlay", back_populates="clip")

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    clip_id = Column(Integer, ForeignKey('clips.id'))
    tag = Column(String(255))

    clip = relationship("Clip")

class Highlight(Base):
    __tablename__ = 'highlights'

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    start_time = Column(Integer)
    end_time = Column(Integer)
    highlight_score = Column(Float)

    video = relationship("Video")

class AIProcessingQueue(Base):
    __tablename__ = 'ai_processing_queue'

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    task_name = Column(String(100))
    status = Column(String(50))
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    video = relationship("Video")

class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False)
    start_time = Column(Float) 
    end_time = Column(Float)

    clips = relationship("Clip", secondary="clip_keywords")

class ClipKeyword(Base):
    __tablename__ = 'clip_keywords'

    clip_id = Column(Integer, ForeignKey('clips.id'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keywords.id'), primary_key=True)

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    clip_id = Column(Integer, ForeignKey('clips.id')) 
    status = Column(String, nullable=False)  # 'pending', 'in_progress', 'completed', 'failed'
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    end_time = Column(DateTime, nullable=True)
    progress = Column(Float, default=0) 
    estimated_time = Column(Float, nullable=True)

    clip = relationship("Clip", backref="jobs")

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String)
    sent_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    read = Column(Boolean, default=False)
    status = Column(String, default="sent")  # Estado: 'sent', 'failed'

    user = relationship("User", backref="notifications")

class TemplatePreset(Base):
    __tablename__ = 'template_presets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    video_id = Column(Integer, ForeignKey('videos.id'))
    settings = Column(JSON)

    video = relationship("Video", backref="template_presets")

#Interactive Models for Video Editor
class TextOverlay(Base):
    __tablename__ = 'text_overlays'

    id = Column(Integer, primary_key=True)
    clip_id = Column(Integer, ForeignKey('clips.id'))
    text = Column(String, nullable=False)
    font = Column(String, nullable=True)
    color = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    position = Column(String, nullable=True)  # e.g. 'top', 'bottom', 'center'
    start_time = Column(Float)  # When the text should appear
    end_time = Column(Float)  # When the text should disappear

    clip = relationship("Clip", back_populates="text_overlays")

class Transition(Base):
    __tablename__ = 'transitions'

    id = Column(Integer, primary_key=True)
    clip_id = Column(Integer, ForeignKey('clips.id'))
    transition_type = Column(String, nullable=False)  # e.g. 'fade', 'slide', 'zoom'
    duration = Column(Float, nullable=False)  # Duration of the transition

    clip = relationship("Clip", back_populates="transitions")

class MusicTrack(Base):
    __tablename__ = 'music_tracks'

    id = Column(Integer, primary_key=True)
    clip_id = Column(Integer, ForeignKey('clips.id'))
    track_name = Column(String, nullable=False)
    track_url = Column(String, nullable=False)  # URL to the track (or path)
    start_time = Column(Float)  # When to start the music
    end_time = Column(Float)  # When to stop the music

    clip = relationship("Clip", back_populates="music_tracks")

class Caption(Base):
    __tablename__ = 'captions'

    id = Column(Integer, primary_key=True)
    clip_id = Column(Integer, ForeignKey('clips.id'))
    text = Column(String, nullable=False)
    start_time = Column(Float)  # When the caption should appear
    end_time = Column(Float)  # When the caption should disappear
    position = Column(String, nullable=True)  # e.g. 'bottom-center', 'top-left'

    clip = relationship("Clip", back_populates="captions")

class EmojiOverlay(Base):
    __tablename__ = 'emoji_overlays'

    id = Column(Integer, primary_key=True)
    clip_id = Column(Integer, ForeignKey('clips.id'))
    emoji = Column(String, nullable=False)  # Emoji character
    start_time = Column(Float)  # When the emoji should appear
    end_time = Column(Float)  # When the emoji should disappear
    position = Column(String, nullable=True)  # e.g. 'top-left', 'center'

    clip = relationship("Clip", back_populates="emoji_overlays")

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # Only if using local auth
    role = Column(String(50), default='user')
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(datetime.timezone.utc), onupdate=datetime.now(datetime.timezone.utc))

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    video_url = Column(String(255), nullable=False)
    video_length = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")

class Clip(Base):
    __tablename__ = 'clips'

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    start_time = Column(Integer)  # Start time in seconds
    end_time = Column(Integer)    # End time in seconds
    clip_url = Column(String(255))
    engagement_score = Column(Float)

    video = relationship("Video")

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

class Caption(Base):
    __tablename__ = 'captions'

    id = Column(Integer, primary_key=True, index=True)
    clip_id = Column(Integer, ForeignKey('clips.id'))
    language = Column(String(10))  # e.g., 'en'
    caption_text = Column(Text)

    clip = relationship("Clip")

class AIProcessingQueue(Base):
    __tablename__ = 'ai_processing_queue'

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    task_name = Column(String(100))
    status = Column(String(50))
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    video = relationship("Video")

"""
数据库模型 - 用户进度和学习记录
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = "sqlite:///./data_analysis_camp.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserProgress(Base):
    """用户进度表"""
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    project_id = Column(Integer, index=True)
    project_name = Column(String)
    score = Column(Float, default=0.0)
    code = Column(Text)
    completed = Column(Integer, default=0)
    attempts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meta_data = Column(JSON, default={})

class LearningRecord(Base):
    """学习记录表"""
    __tablename__ = "learning_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    project_id = Column(Integer)
    action = Column(String)  # run_code, get_hint, submit_answer
    code = Column(Text)
    result = Column(JSON)
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Leaderboard(Base):
    """排行榜表"""
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    project_id = Column(Integer, index=True)
    score = Column(Float)
    metric_name = Column(String)  # MSE, accuracy等
    meta_data = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

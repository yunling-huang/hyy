"""
Pydantic模式定义
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CodeRunRequest(BaseModel):
    """代码执行请求"""
    project_id: int
    user_id: str
    code: str
    language: str = "python"

class CodeRunResponse(BaseModel):
    """代码执行响应"""
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0

class ScoreRequest(BaseModel):
    """评分请求"""
    project_id: int
    user_id: str
    code: str
    result: Dict[str, Any]

class ScoreResponse(BaseModel):
    """评分响应"""
    score: float
    max_score: float
    feedback: str
    hints: List[str] = []

class ProgressRequest(BaseModel):
    """进度保存请求"""
    user_id: str
    project_id: int
    project_name: str
    code: str
    score: float
    completed: bool
    metadata: Dict[str, Any] = {}

class ProgressResponse(BaseModel):
    """进度响应"""
    success: bool
    message: str

class LeaderboardEntry(BaseModel):
    """排行榜条目"""
    user_id: str
    score: float
    metric_name: str
    rank: int

class ProjectInfo(BaseModel):
    """项目信息"""
    id: int
    name: str
    description: str
    category: str
    difficulty: str
    estimated_time: str

class AIFeedbackRequest(BaseModel):
    """AI反馈请求"""
    project_id: int
    user_code: str
    execution_result: Dict[str, Any]

class AIFeedbackResponse(BaseModel):
    """AI反馈响应"""
    feedback: str
    suggestions: List[str] = []
    code_quality_score: float = 0.0

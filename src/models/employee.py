from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum


class SkillLevel(str, Enum):
    """スキルレベルの定義"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Department(str, Enum):
    """部署の定義"""
    ENGINEERING = "engineering"
    SALES = "sales"
    MARKETING = "marketing"
    HR = "hr"
    FINANCE = "finance"
    OPERATIONS = "operations"


class Skill(BaseModel):
    """スキル情報"""
    name: str
    level: SkillLevel
    last_assessed: datetime
    progress_rate: float = Field(ge=0.0, le=100.0)


class PerformanceMetric(BaseModel):
    """パフォーマンス指標"""
    metric_name: str
    value: float
    target_value: float
    achieved_date: datetime
    category: str


class Employee(BaseModel):
    """新人社員のデータモデル"""
    id: str
    name: str
    email: str
    department: Department
    hire_date: datetime
    mentor_id: Optional[str] = None
    
    # スキル関連
    skills: List[Skill] = []
    learning_pace: float = Field(default=1.0, ge=0.1, le=3.0)
    preferred_learning_style: str = "visual"
    
    # パフォーマンス関連
    performance_metrics: List[PerformanceMetric] = []
    overall_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    
    # 特性
    strengths: List[str] = []
    improvement_areas: List[str] = []
    personality_traits: Dict[str, float] = {}
    
    # 学習履歴
    completed_trainings: List[str] = []
    current_objectives: List[str] = []
    
    # メタデータ
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
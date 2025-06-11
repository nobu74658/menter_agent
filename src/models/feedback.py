from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum


class FeedbackType(str, Enum):
    """フィードバックタイプ"""
    POSITIVE = "positive"
    CONSTRUCTIVE = "constructive"
    DEVELOPMENTAL = "developmental"
    RECOGNITION = "recognition"


class Priority(str, Enum):
    """優先度"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ActionItem(BaseModel):
    """アクションアイテム"""
    description: str
    due_date: Optional[datetime] = None
    priority: Priority = Priority.MEDIUM
    resources: List[str] = []
    estimated_hours: Optional[float] = None
    completed: bool = False


class Feedback(BaseModel):
    """フィードバックモデル"""
    id: str
    employee_id: str
    mentor_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    # フィードバック内容
    type: FeedbackType
    category: str  # technical, communication, teamwork, etc.
    summary: str
    detailed_feedback: str
    
    # 評価
    impact_score: float = Field(ge=0.0, le=10.0)
    confidence_level: float = Field(ge=0.0, le=1.0)
    
    # 具体例
    specific_examples: List[str] = []
    observed_behaviors: List[str] = []
    
    # 推奨事項
    recommendations: List[str] = []
    action_items: List[ActionItem] = []
    suggested_resources: List[Dict[str, str]] = []
    
    # 成長指標
    skill_improvements: Dict[str, float] = {}
    expected_timeline: Optional[str] = None
    
    # メタデータ
    is_automated: bool = True
    employee_acknowledged: bool = False
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
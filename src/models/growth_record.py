from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class MilestoneStatus(str, Enum):
    """マイルストーンステータス"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"


class GrowthTrend(str, Enum):
    """成長トレンド"""
    RAPID = "rapid"
    STEADY = "steady"
    SLOW = "slow"
    STAGNANT = "stagnant"
    DECLINING = "declining"


class Milestone(BaseModel):
    """成長マイルストーン"""
    name: str
    description: str
    target_date: datetime
    completion_date: Optional[datetime] = None
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED
    achievement_criteria: List[str] = []
    evidence: List[str] = []


class SkillProgress(BaseModel):
    """スキル進捗"""
    skill_name: str
    initial_level: float
    current_level: float
    target_level: float
    progress_percentage: float = Field(ge=0.0, le=100.0)
    last_assessment_date: datetime
    improvement_rate: float  # per month


class GrowthRecord(BaseModel):
    """成長記録モデル"""
    id: str
    employee_id: str
    period_start: datetime
    period_end: datetime
    
    # 全体的な成長指標
    overall_growth_score: float = Field(ge=0.0, le=10.0)
    growth_trend: GrowthTrend
    
    # スキル別進捗
    skill_progress: List[SkillProgress] = []
    
    # マイルストーン
    milestones: List[Milestone] = []
    completed_objectives: List[str] = []
    
    # 成果と課題
    key_achievements: List[str] = []
    challenges_faced: List[str] = []
    lessons_learned: List[str] = []
    
    # フィードバック履歴
    feedback_ids: List[str] = []
    feedback_implementation_rate: float = Field(ge=0.0, le=100.0)
    
    # 比較分析
    peer_comparison: Optional[Dict[str, float]] = None
    department_average_comparison: Optional[float] = None
    
    # 予測と推奨
    predicted_growth_rate: float
    recommended_focus_areas: List[str] = []
    risk_indicators: List[str] = []
    
    # メタデータ
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    reviewed_by: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
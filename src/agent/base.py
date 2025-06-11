from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from ..models import Employee, Feedback, GrowthRecord


class BaseMentorAgent(ABC):
    """メンターエージェントの基底クラス"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.initialize()
    
    @abstractmethod
    def initialize(self):
        """エージェントの初期化"""
        pass
    
    @abstractmethod
    def analyze_employee(self, employee: Employee) -> Dict[str, Any]:
        """社員の分析を実行"""
        pass
    
    @abstractmethod
    def generate_feedback(self, employee: Employee, context: Optional[Dict[str, Any]] = None) -> Feedback:
        """フィードバックを生成"""
        pass
    
    @abstractmethod
    def create_growth_plan(self, employee: Employee, timeframe: int = 90) -> Dict[str, Any]:
        """成長計画を作成"""
        pass
    
    @abstractmethod
    def track_progress(self, employee: Employee, start_date: datetime, end_date: datetime) -> GrowthRecord:
        """進捗をトラッキング"""
        pass
    
    @abstractmethod
    def provide_support(self, employee: Employee, issue_type: str) -> Dict[str, Any]:
        """サポートを提供"""
        pass
    
    def assess_learning_needs(self, employee: Employee) -> List[str]:
        """学習ニーズを評価"""
        needs = []
        
        # スキルギャップの分析
        for skill in employee.skills:
            if skill.progress_rate < 50:
                needs.append(f"Improve {skill.name} skills")
        
        # 改善領域に基づくニーズ
        for area in employee.improvement_areas:
            needs.append(f"Address {area}")
        
        return needs
    
    def calculate_growth_score(self, employee: Employee) -> float:
        """成長スコアを計算"""
        if not employee.performance_metrics:
            return 0.0
        
        achieved_metrics = [
            m for m in employee.performance_metrics 
            if m.value >= m.target_value
        ]
        
        score = len(achieved_metrics) / len(employee.performance_metrics) * 10
        return round(score, 2)
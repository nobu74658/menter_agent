from typing import List, Dict, Any
from datetime import datetime, timedelta
import statistics

from ..models import Employee, SkillLevel


class AnalysisService:
    """社員分析サービス"""
    
    def analyze_skill_distribution(self, employee: Employee) -> Dict[str, Any]:
        """スキル分布を分析"""
        if not employee.skills:
            return {"status": "no_skills_recorded"}
        
        skill_levels = {
            SkillLevel.BEGINNER: 0,
            SkillLevel.INTERMEDIATE: 0,
            SkillLevel.ADVANCED: 0,
            SkillLevel.EXPERT: 0
        }
        
        for skill in employee.skills:
            skill_levels[skill.level] += 1
        
        return {
            "distribution": skill_levels,
            "dominant_level": max(skill_levels, key=skill_levels.get),
            "total_skills": len(employee.skills)
        }
    
    def calculate_performance_trend(self, employee: Employee, days: int = 30) -> Dict[str, Any]:
        """パフォーマンストレンドを計算"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_metrics = [
            m for m in employee.performance_metrics 
            if m.achieved_date >= cutoff_date
        ]
        
        if not recent_metrics:
            return {"trend": "no_data", "improvement_rate": 0}
        
        achievement_rates = [
            (m.value / m.target_value * 100) if m.target_value > 0 else 0
            for m in recent_metrics
        ]
        
        avg_achievement = statistics.mean(achievement_rates) if achievement_rates else 0
        
        if avg_achievement > 100:
            trend = "exceeding"
        elif avg_achievement > 80:
            trend = "meeting"
        elif avg_achievement > 60:
            trend = "approaching"
        else:
            trend = "below"
        
        return {
            "trend": trend,
            "average_achievement": round(avg_achievement, 2),
            "metrics_count": len(recent_metrics)
        }
    
    def identify_learning_patterns(self, employee: Employee) -> Dict[str, Any]:
        """学習パターンを特定"""
        patterns = {
            "preferred_style": employee.preferred_learning_style,
            "learning_pace": employee.learning_pace,
            "consistency": self._calculate_learning_consistency(employee),
            "engagement_level": self._assess_engagement_level(employee)
        }
        
        return patterns
    
    def compare_with_peers(self, employee: Employee, peer_group: List[Employee]) -> Dict[str, Any]:
        """同僚との比較分析"""
        if not peer_group:
            return {"status": "no_peers_for_comparison"}
        
        employee_score = self._calculate_overall_score(employee)
        peer_scores = [self._calculate_overall_score(peer) for peer in peer_group]
        avg_peer_score = statistics.mean(peer_scores) if peer_scores else 0
        
        percentile = sum(1 for score in peer_scores if employee_score > score) / len(peer_scores) * 100
        
        return {
            "employee_score": employee_score,
            "peer_average": round(avg_peer_score, 2),
            "percentile": round(percentile, 1),
            "comparison": "above_average" if employee_score > avg_peer_score else "below_average"
        }
    
    def predict_readiness_for_advancement(self, employee: Employee) -> Dict[str, Any]:
        """昇進準備度を予測"""
        readiness_factors = {
            "skill_readiness": self._assess_skill_readiness(employee),
            "performance_consistency": self._assess_performance_consistency(employee),
            "growth_rate": self._calculate_growth_rate(employee),
            "leadership_potential": self._assess_leadership_potential(employee)
        }
        
        overall_readiness = sum(readiness_factors.values()) / len(readiness_factors)
        
        return {
            "overall_readiness": round(overall_readiness, 2),
            "factors": readiness_factors,
            "recommendation": "ready" if overall_readiness > 75 else "needs_development"
        }
    
    def _calculate_learning_consistency(self, employee: Employee) -> float:
        """学習の一貫性を計算"""
        if not employee.completed_trainings:
            return 0.0
        
        # 完了したトレーニングの数に基づく簡単な計算
        consistency_score = min(len(employee.completed_trainings) * 10, 100)
        return float(consistency_score)
    
    def _assess_engagement_level(self, employee: Employee) -> str:
        """エンゲージメントレベルを評価"""
        indicators = 0
        
        if employee.current_objectives:
            indicators += 1
        if employee.completed_trainings:
            indicators += 1
        if employee.skills and any(s.progress_rate > 70 for s in employee.skills):
            indicators += 1
        
        if indicators >= 3:
            return "high"
        elif indicators >= 2:
            return "medium"
        else:
            return "low"
    
    def _calculate_overall_score(self, employee: Employee) -> float:
        """総合スコアを計算"""
        score_components = []
        
        # スキルスコア
        if employee.skills:
            skill_score = sum(s.progress_rate for s in employee.skills) / len(employee.skills)
            score_components.append(skill_score)
        
        # パフォーマンススコア
        if employee.overall_rating:
            score_components.append(employee.overall_rating * 20)  # 5点満点を100点換算
        
        # 学習ペーススコア
        score_components.append(min(employee.learning_pace * 50, 100))
        
        return statistics.mean(score_components) if score_components else 0
    
    def _assess_skill_readiness(self, employee: Employee) -> float:
        """スキル準備度を評価"""
        if not employee.skills:
            return 0.0
        
        advanced_skills = sum(1 for s in employee.skills if s.level in [SkillLevel.ADVANCED, SkillLevel.EXPERT])
        return (advanced_skills / len(employee.skills)) * 100
    
    def _assess_performance_consistency(self, employee: Employee) -> float:
        """パフォーマンスの一貫性を評価"""
        if not employee.performance_metrics:
            return 0.0
        
        achievement_rates = [
            (m.value / m.target_value * 100) if m.target_value > 0 else 0
            for m in employee.performance_metrics
        ]
        
        if len(achievement_rates) < 2:
            return achievement_rates[0] if achievement_rates else 0.0
        
        # 標準偏差が低いほど一貫性が高い
        std_dev = statistics.stdev(achievement_rates)
        consistency = max(0, 100 - std_dev)
        
        return consistency
    
    def _calculate_growth_rate(self, employee: Employee) -> float:
        """成長率を計算"""
        base_rate = employee.learning_pace * 50
        
        # スキルの進歩率も考慮
        if employee.skills:
            avg_progress = sum(s.progress_rate for s in employee.skills) / len(employee.skills)
            base_rate = (base_rate + avg_progress) / 2
        
        return min(base_rate, 100)
    
    def _assess_leadership_potential(self, employee: Employee) -> float:
        """リーダーシップポテンシャルを評価"""
        potential_score = 50.0  # ベースライン
        
        # 強みに基づく評価
        leadership_traits = ["communication", "problem-solving", "teamwork", "initiative"]
        matching_strengths = sum(1 for trait in leadership_traits if any(trait in s.lower() for s in employee.strengths))
        potential_score += matching_strengths * 10
        
        # パーソナリティ特性に基づく評価
        if "leadership" in employee.personality_traits:
            potential_score += employee.personality_traits["leadership"] * 20
        
        return min(potential_score, 100)
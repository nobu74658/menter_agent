from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import math

from ..models import Employee, GrowthTrend, SkillLevel


class GrowthService:
    """成長管理サービス"""
    
    def calculate_growth_trajectory(self, employee: Employee, 
                                  historical_data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """成長軌道を計算"""
        current_score = self._calculate_current_score(employee)
        
        if not historical_data:
            # 履歴データがない場合は現在のデータから推定
            projected_score = current_score * (1 + employee.learning_pace * 0.1)
            growth_rate = employee.learning_pace * 10
        else:
            # 履歴データから実際の成長率を計算
            past_scores = [data.get("score", 0) for data in historical_data]
            growth_rate = self._calculate_growth_rate_from_history(past_scores + [current_score])
            projected_score = current_score * (1 + growth_rate / 100)
        
        trajectory = {
            "current_score": round(current_score, 2),
            "projected_score_3_months": round(projected_score, 2),
            "growth_rate_monthly": round(growth_rate, 2),
            "trend": self._determine_trend(growth_rate),
            "confidence_level": 0.8 if historical_data else 0.6
        }
        
        return trajectory
    
    def create_personalized_growth_plan(self, employee: Employee) -> Dict[str, Any]:
        """個別化された成長計画を作成"""
        skill_gaps = self._identify_skill_gaps(employee)
        learning_recommendations = self._generate_learning_recommendations(employee, skill_gaps)
        milestones = self._create_growth_milestones(employee, skill_gaps)
        
        growth_plan = {
            "employee_id": employee.id,
            "created_date": datetime.now().isoformat(),
            "duration_months": 6,
            "primary_objectives": self._define_primary_objectives(employee),
            "skill_development_plan": skill_gaps,
            "learning_path": learning_recommendations,
            "milestones": milestones,
            "support_requirements": self._identify_support_needs(employee),
            "success_metrics": self._define_success_metrics(employee),
            "risk_mitigation": self._identify_risks_and_mitigation(employee)
        }
        
        return growth_plan
    
    def track_milestone_progress(self, employee: Employee, milestone_id: str) -> Dict[str, Any]:
        """マイルストーンの進捗を追跡"""
        # 実際の実装では、データベースからマイルストーンを取得
        milestone_progress = {
            "milestone_id": milestone_id,
            "status": "in_progress",
            "completion_percentage": 65,
            "blockers": self._identify_blockers(employee),
            "achievements": self._list_recent_achievements(employee),
            "next_actions": self._suggest_next_actions(employee),
            "estimated_completion": (datetime.now() + timedelta(days=14)).isoformat()
        }
        
        return milestone_progress
    
    def generate_growth_insights(self, employee: Employee, period_days: int = 90) -> Dict[str, Any]:
        """成長に関する洞察を生成"""
        insights = {
            "key_insights": [],
            "growth_patterns": self._analyze_growth_patterns(employee),
            "breakthrough_moments": self._identify_breakthroughs(employee),
            "plateau_areas": self._identify_plateaus(employee),
            "acceleration_opportunities": self._find_acceleration_opportunities(employee)
        }
        
        # 主要な洞察を生成
        if employee.learning_pace > 1.5:
            insights["key_insights"].append("Fast learner - consider accelerated program")
        
        if len(employee.improvement_areas) > len(employee.strengths):
            insights["key_insights"].append("Focus on building confidence in strength areas")
        
        skill_diversity = len(set(s.level for s in employee.skills))
        if skill_diversity > 2:
            insights["key_insights"].append("Diverse skill levels - consider specialization")
        
        return insights
    
    def recommend_interventions(self, employee: Employee, 
                              growth_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """成長を促進する介入を推奨"""
        interventions = []
        
        # 成長率に基づく介入
        if growth_data.get("growth_rate_monthly", 0) < 5:
            interventions.append({
                "type": "learning_acceleration",
                "priority": "high",
                "action": "Pair with high-performing mentor",
                "expected_impact": "20% increase in learning speed",
                "timeline": "2 weeks"
            })
        
        # スキルギャップに基づく介入
        if any(s.progress_rate < 40 for s in employee.skills):
            interventions.append({
                "type": "skill_development",
                "priority": "high",
                "action": "Intensive skill workshop",
                "expected_impact": "Close critical skill gaps",
                "timeline": "1 month"
            })
        
        # モチベーションに基づく介入
        if employee.learning_pace < 0.8:
            interventions.append({
                "type": "motivation_boost",
                "priority": "medium",
                "action": "Success story sharing session",
                "expected_impact": "Increase engagement",
                "timeline": "1 week"
            })
        
        return interventions
    
    def _calculate_current_score(self, employee: Employee) -> float:
        """現在のスコアを計算"""
        components = []
        
        # スキルコンポーネント
        if employee.skills:
            avg_skill_progress = sum(s.progress_rate for s in employee.skills) / len(employee.skills)
            components.append(avg_skill_progress)
        
        # パフォーマンスコンポーネント
        if employee.overall_rating:
            components.append(employee.overall_rating * 20)
        
        # 学習ペースコンポーネント
        components.append(min(employee.learning_pace * 40, 100))
        
        return sum(components) / len(components) if components else 50.0
    
    def _calculate_growth_rate_from_history(self, scores: List[float]) -> float:
        """履歴から成長率を計算"""
        if len(scores) < 2:
            return 0.0
        
        # 線形回帰的なアプローチで成長率を計算
        n = len(scores)
        x_mean = (n - 1) / 2
        y_mean = sum(scores) / n
        
        numerator = sum((i - x_mean) * (score - y_mean) for i, score in enumerate(scores))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        slope = numerator / denominator
        return slope * 10  # 月次成長率として調整
    
    def _determine_trend(self, growth_rate: float) -> str:
        """成長トレンドを判定"""
        if growth_rate > 15:
            return "rapid_growth"
        elif growth_rate > 8:
            return "steady_growth"
        elif growth_rate > 2:
            return "slow_growth"
        elif growth_rate > -2:
            return "stagnant"
        else:
            return "declining"
    
    def _identify_skill_gaps(self, employee: Employee) -> List[Dict[str, Any]]:
        """スキルギャップを特定"""
        gaps = []
        
        # 現在のスキルで進捗が低いもの
        for skill in employee.skills:
            if skill.progress_rate < 60:
                gaps.append({
                    "skill": skill.name,
                    "current_level": skill.level.value,
                    "gap_size": 60 - skill.progress_rate,
                    "priority": "high" if skill.progress_rate < 40 else "medium"
                })
        
        # 部署に必要だが持っていないスキル
        required_skills = self._get_required_skills_for_department(employee.department)
        current_skill_names = [s.name for s in employee.skills]
        
        for req_skill in required_skills:
            if req_skill not in current_skill_names:
                gaps.append({
                    "skill": req_skill,
                    "current_level": "not_acquired",
                    "gap_size": 100,
                    "priority": "high"
                })
        
        return sorted(gaps, key=lambda x: x["gap_size"], reverse=True)[:5]
    
    def _get_required_skills_for_department(self, department: str) -> List[str]:
        """部署に必要なスキルを取得"""
        department_skills = {
            "engineering": ["Programming", "System Design", "Testing", "Debugging"],
            "sales": ["Communication", "Negotiation", "Product Knowledge", "CRM"],
            "marketing": ["Content Creation", "Analytics", "Social Media", "SEO"],
            "hr": ["Recruiting", "Employee Relations", "Training", "Compliance"],
            "finance": ["Accounting", "Financial Analysis", "Excel", "Reporting"],
            "operations": ["Process Management", "Quality Control", "Logistics", "Planning"]
        }
        
        return department_skills.get(department.value, ["Communication", "Problem Solving", "Teamwork"])
    
    def _generate_learning_recommendations(self, employee: Employee, 
                                         skill_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """学習推奨事項を生成"""
        recommendations = []
        
        for gap in skill_gaps[:3]:  # トップ3のギャップに焦点
            recommendation = {
                "skill": gap["skill"],
                "learning_method": self._select_learning_method(employee, gap["skill"]),
                "resources": self._suggest_learning_resources(gap["skill"]),
                "estimated_time": f"{gap['gap_size'] // 10 * 10} hours",
                "practice_opportunities": self._identify_practice_opportunities(gap["skill"])
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def _select_learning_method(self, employee: Employee, skill: str) -> str:
        """最適な学習方法を選択"""
        if employee.preferred_learning_style == "visual":
            return "Video tutorials and infographics"
        elif employee.preferred_learning_style == "hands-on":
            return "Practical projects and exercises"
        elif employee.preferred_learning_style == "reading":
            return "Books and documentation"
        else:
            return "Mixed approach with mentoring"
    
    def _suggest_learning_resources(self, skill: str) -> List[str]:
        """学習リソースを提案"""
        # 実際の実装では、スキルデータベースから取得
        return [
            f"Online course: Mastering {skill}",
            f"Book: {skill} Best Practices",
            f"Workshop: Hands-on {skill} Training"
        ]
    
    def _identify_practice_opportunities(self, skill: str) -> List[str]:
        """実践機会を特定"""
        return [
            f"Join project requiring {skill}",
            f"Shadow expert in {skill}",
            f"Complete {skill} certification"
        ]
    
    def _create_growth_milestones(self, employee: Employee, 
                                 skill_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """成長マイルストーンを作成"""
        milestones = []
        
        # 30日ごとのマイルストーン
        for i in range(1, 7):  # 6ヶ月分
            milestone = {
                "month": i,
                "target_date": (datetime.now() + timedelta(days=30*i)).isoformat(),
                "objectives": self._define_monthly_objectives(employee, i, skill_gaps),
                "success_criteria": self._define_success_criteria(i),
                "checkpoint_activities": ["Progress review", "Skill assessment", "Feedback session"]
            }
            milestones.append(milestone)
        
        return milestones
    
    def _define_monthly_objectives(self, employee: Employee, month: int, 
                                  skill_gaps: List[Dict[str, Any]]) -> List[str]:
        """月次目標を定義"""
        if month <= 2:
            return ["Foundation building", "Basic skill acquisition"]
        elif month <= 4:
            return ["Skill application", "Independent task completion"]
        else:
            return ["Advanced skill development", "Mentoring others"]
    
    def _define_success_criteria(self, month: int) -> List[str]:
        """成功基準を定義"""
        base_criteria = ["Complete assigned learning modules", "Apply skills in real work"]
        
        if month >= 3:
            base_criteria.append("Receive positive peer feedback")
        if month >= 6:
            base_criteria.append("Lead a small project independently")
        
        return base_criteria
    
    def _define_primary_objectives(self, employee: Employee) -> List[str]:
        """主要目標を定義"""
        objectives = []
        
        # スキルベースの目標
        low_skills = [s for s in employee.skills if s.progress_rate < 50]
        for skill in low_skills[:2]:
            objectives.append(f"Improve {skill.name} to intermediate level")
        
        # 改善領域ベースの目標
        for area in employee.improvement_areas[:2]:
            objectives.append(f"Address {area} through targeted development")
        
        # 一般的な成長目標
        objectives.append("Increase overall performance rating by 20%")
        
        return objectives[:5]
    
    def _identify_support_needs(self, employee: Employee) -> List[str]:
        """サポートニーズを特定"""
        needs = ["Regular mentoring sessions"]
        
        if employee.learning_pace < 1.0:
            needs.append("Additional one-on-one support")
        
        if len(employee.improvement_areas) > 3:
            needs.append("Focused coaching on priority areas")
        
        if not employee.current_objectives:
            needs.append("Goal-setting workshop")
        
        return needs
    
    def _define_success_metrics(self, employee: Employee) -> Dict[str, Any]:
        """成功指標を定義"""
        return {
            "skill_improvement": "30% increase in average skill progress",
            "performance_rating": "Achieve 4.0+ rating",
            "project_completion": "Complete 5+ projects independently",
            "peer_feedback": "Receive 85%+ positive feedback",
            "learning_completion": "Complete 100% of assigned training"
        }
    
    def _identify_risks_and_mitigation(self, employee: Employee) -> List[Dict[str, str]]:
        """リスクと緩和策を特定"""
        risks = []
        
        if employee.learning_pace < 0.7:
            risks.append({
                "risk": "Slow progress may impact motivation",
                "mitigation": "Provide frequent encouragement and small wins"
            })
        
        if len(employee.skills) > 10:
            risks.append({
                "risk": "Too many focus areas may dilute progress",
                "mitigation": "Prioritize top 3-5 skills for focused development"
            })
        
        return risks
    
    def _identify_blockers(self, employee: Employee) -> List[str]:
        """ブロッカーを特定"""
        blockers = []
        
        if employee.learning_pace < 0.5:
            blockers.append("Learning pace significantly below average")
        
        if not employee.mentor_id:
            blockers.append("No assigned mentor")
        
        return blockers
    
    def _list_recent_achievements(self, employee: Employee) -> List[str]:
        """最近の成果をリスト化"""
        achievements = []
        
        # 高進捗のスキル
        for skill in employee.skills:
            if skill.progress_rate > 80:
                achievements.append(f"Achieved proficiency in {skill.name}")
        
        # 完了したトレーニング
        if employee.completed_trainings:
            achievements.append(f"Completed {len(employee.completed_trainings)} training modules")
        
        return achievements[:5]
    
    def _suggest_next_actions(self, employee: Employee) -> List[str]:
        """次のアクションを提案"""
        actions = []
        
        # 低進捗スキルへの対応
        low_progress_skills = [s for s in employee.skills if s.progress_rate < 50]
        if low_progress_skills:
            actions.append(f"Focus on improving {low_progress_skills[0].name}")
        
        # 現在の目標への取り組み
        if employee.current_objectives:
            actions.append(f"Continue working on: {employee.current_objectives[0]}")
        
        return actions
    
    def _analyze_growth_patterns(self, employee: Employee) -> Dict[str, Any]:
        """成長パターンを分析"""
        return {
            "consistency": "high" if employee.learning_pace > 0.8 else "low",
            "acceleration_points": ["After mentoring sessions", "During team projects"],
            "deceleration_points": ["Heavy workload periods", "Lack of clear objectives"]
        }
    
    def _identify_breakthroughs(self, employee: Employee) -> List[str]:
        """ブレークスルーを特定"""
        breakthroughs = []
        
        for skill in employee.skills:
            if skill.progress_rate > 85:
                breakthroughs.append(f"Breakthrough in {skill.name}")
        
        return breakthroughs
    
    def _identify_plateaus(self, employee: Employee) -> List[str]:
        """停滞領域を特定"""
        plateaus = []
        
        for skill in employee.skills:
            if 40 < skill.progress_rate < 60:
                plateaus.append(f"{skill.name} progress has plateaued")
        
        return plateaus
    
    def _find_acceleration_opportunities(self, employee: Employee) -> List[str]:
        """加速機会を見つける"""
        opportunities = []
        
        if employee.learning_pace > 1.2:
            opportunities.append("Ready for advanced challenges")
        
        if len(employee.strengths) > 3:
            opportunities.append("Leverage strengths for rapid skill transfer")
        
        return opportunities
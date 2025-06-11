from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import json
from pathlib import Path

from .base import BaseMentorAgent
from ..models import (
    Employee, Feedback, GrowthRecord, 
    FeedbackType, Priority, ActionItem,
    SkillProgress, Milestone, MilestoneStatus,
    GrowthTrend
)
from ..services.analysis_service import AnalysisService
from ..services.feedback_service import FeedbackService
from ..services.growth_service import GrowthService


class MentorAgent(BaseMentorAgent):
    """メンターエージェントの実装"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.analysis_service = AnalysisService()
        self.feedback_service = FeedbackService()
        self.growth_service = GrowthService()
        
    def initialize(self):
        """エージェントの初期化"""
        self.logger.info("Initializing MentorAgent")
        # データディレクトリの確認
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        (self.data_dir / "employees").mkdir(exist_ok=True)
        (self.data_dir / "feedbacks").mkdir(exist_ok=True)
    
    def analyze_employee(self, employee: Employee) -> Dict[str, Any]:
        """社員の詳細分析を実行"""
        analysis = {
            "employee_id": employee.id,
            "name": employee.name,
            "tenure_days": (datetime.now() - employee.hire_date).days,
            "overall_assessment": self._assess_overall_performance(employee),
            "skill_analysis": self._analyze_skills(employee),
            "growth_trajectory": self._determine_growth_trajectory(employee),
            "risk_factors": self._identify_risk_factors(employee),
            "recommendations": self._generate_recommendations(employee)
        }
        
        return analysis
    
    def generate_feedback(self, employee: Employee, context: Optional[Dict[str, Any]] = None) -> Feedback:
        """個別化されたフィードバックを生成"""
        # 分析結果を取得
        analysis = self.analyze_employee(employee)
        
        # フィードバックタイプの決定
        feedback_type = self._determine_feedback_type(analysis)
        
        # フィードバック内容の生成
        feedback_content = self._create_feedback_content(employee, analysis, feedback_type)
        
        # アクションアイテムの生成
        action_items = self._generate_action_items(employee, analysis)
        
        feedback = Feedback(
            id=str(uuid.uuid4()),
            employee_id=employee.id,
            mentor_id="mentor_agent_001",
            type=feedback_type,
            category=self._determine_feedback_category(employee),
            summary=feedback_content["summary"],
            detailed_feedback=feedback_content["detailed"],
            impact_score=feedback_content["impact_score"],
            confidence_level=0.85,
            specific_examples=feedback_content["examples"],
            observed_behaviors=feedback_content["behaviors"],
            recommendations=feedback_content["recommendations"],
            action_items=action_items,
            skill_improvements=self._calculate_skill_improvements(employee),
            expected_timeline="30-60 days",
            follow_up_required=len(action_items) > 0
        )
        
        # フィードバックを保存
        self._save_feedback(feedback)
        
        return feedback
    
    def create_growth_plan(self, employee: Employee, timeframe: int = 90) -> Dict[str, Any]:
        """カスタマイズされた成長計画を作成"""
        analysis = self.analyze_employee(employee)
        
        growth_plan = {
            "employee_id": employee.id,
            "timeframe_days": timeframe,
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=timeframe)).isoformat(),
            "objectives": self._define_growth_objectives(employee, analysis),
            "milestones": self._create_milestones(employee, timeframe),
            "learning_path": self._design_learning_path(employee),
            "support_mechanisms": self._identify_support_mechanisms(employee),
            "success_metrics": self._define_success_metrics(employee),
            "review_schedule": self._create_review_schedule(timeframe)
        }
        
        return growth_plan
    
    def track_progress(self, employee: Employee, start_date: datetime, end_date: datetime) -> GrowthRecord:
        """社員の進捗をトラッキング"""
        # スキル進捗の計算
        skill_progress = self._calculate_skill_progress(employee, start_date, end_date)
        
        # 成長トレンドの判定
        growth_trend = self._determine_growth_trend(skill_progress)
        
        # マイルストーンの確認
        milestones = self._check_milestones(employee, start_date, end_date)
        
        growth_record = GrowthRecord(
            id=str(uuid.uuid4()),
            employee_id=employee.id,
            period_start=start_date,
            period_end=end_date,
            overall_growth_score=self.calculate_growth_score(employee),
            growth_trend=growth_trend,
            skill_progress=skill_progress,
            milestones=milestones,
            completed_objectives=employee.completed_trainings,
            key_achievements=self._identify_achievements(employee, start_date, end_date),
            challenges_faced=self._identify_challenges(employee),
            lessons_learned=self._extract_lessons_learned(employee),
            feedback_implementation_rate=self._calculate_feedback_implementation_rate(employee),
            predicted_growth_rate=self._predict_growth_rate(employee),
            recommended_focus_areas=self._recommend_focus_areas(employee),
            risk_indicators=self._identify_risk_indicators(employee)
        )
        
        return growth_record
    
    def provide_support(self, employee: Employee, issue_type: str) -> Dict[str, Any]:
        """状況に応じたサポートを提供"""
        support_response = {
            "employee_id": employee.id,
            "issue_type": issue_type,
            "timestamp": datetime.now().isoformat(),
            "support_provided": []
        }
        
        if issue_type == "skill_gap":
            support_response["support_provided"] = self._provide_skill_support(employee)
        elif issue_type == "motivation":
            support_response["support_provided"] = self._provide_motivation_support(employee)
        elif issue_type == "communication":
            support_response["support_provided"] = self._provide_communication_support(employee)
        elif issue_type == "workload":
            support_response["support_provided"] = self._provide_workload_support(employee)
        else:
            support_response["support_provided"] = self._provide_general_support(employee)
        
        support_response["follow_up_actions"] = self._generate_follow_up_actions(employee, issue_type)
        support_response["resources"] = self._recommend_resources(employee, issue_type)
        
        return support_response
    
    # ヘルパーメソッド
    def _assess_overall_performance(self, employee: Employee) -> str:
        score = self.calculate_growth_score(employee)
        if score >= 8:
            return "Excellent"
        elif score >= 6:
            return "Good"
        elif score >= 4:
            return "Satisfactory"
        else:
            return "Needs Improvement"
    
    def _analyze_skills(self, employee: Employee) -> Dict[str, Any]:
        return {
            "total_skills": len(employee.skills),
            "average_progress": sum(s.progress_rate for s in employee.skills) / len(employee.skills) if employee.skills else 0,
            "skills_needing_attention": [s.name for s in employee.skills if s.progress_rate < 50]
        }
    
    def _determine_growth_trajectory(self, employee: Employee) -> str:
        # 簡略化された成長軌道の判定
        if employee.learning_pace > 1.5:
            return "Accelerated"
        elif employee.learning_pace > 0.8:
            return "Normal"
        else:
            return "Slow"
    
    def _identify_risk_factors(self, employee: Employee) -> List[str]:
        risks = []
        if employee.learning_pace < 0.5:
            risks.append("Very slow learning pace")
        if len(employee.improvement_areas) > 5:
            risks.append("Multiple improvement areas")
        if not employee.current_objectives:
            risks.append("No clear objectives set")
        return risks
    
    def _generate_recommendations(self, employee: Employee) -> List[str]:
        recommendations = []
        for area in employee.improvement_areas[:3]:  # Top 3 areas
            recommendations.append(f"Focus on improving {area}")
        if employee.learning_pace < 1.0:
            recommendations.append("Consider adjusting learning approach")
        return recommendations
    
    def _determine_feedback_type(self, analysis: Dict[str, Any]) -> FeedbackType:
        if analysis["overall_assessment"] == "Excellent":
            return FeedbackType.RECOGNITION
        elif len(analysis["risk_factors"]) > 2:
            return FeedbackType.DEVELOPMENTAL
        else:
            return FeedbackType.CONSTRUCTIVE
    
    def _create_feedback_content(self, employee: Employee, analysis: Dict[str, Any], 
                                feedback_type: FeedbackType) -> Dict[str, Any]:
        return {
            "summary": f"Performance feedback for {employee.name}",
            "detailed": f"Based on analysis, your overall performance is {analysis['overall_assessment']}. "
                       f"Your growth trajectory appears to be {analysis['growth_trajectory']}.",
            "impact_score": self.calculate_growth_score(employee),
            "examples": [f"Demonstrated progress in {s.name}" for s in employee.skills if s.progress_rate > 70],
            "behaviors": employee.strengths[:3],
            "recommendations": analysis["recommendations"]
        }
    
    def _generate_action_items(self, employee: Employee, analysis: Dict[str, Any]) -> List[ActionItem]:
        action_items = []
        for i, rec in enumerate(analysis["recommendations"][:3]):
            action_items.append(ActionItem(
                description=rec,
                due_date=datetime.now() + timedelta(days=30 * (i + 1)),
                priority=Priority.HIGH if i == 0 else Priority.MEDIUM,
                estimated_hours=20.0
            ))
        return action_items
    
    def _determine_feedback_category(self, employee: Employee) -> str:
        if employee.department in ["engineering", "technical"]:
            return "technical"
        elif employee.department in ["sales", "marketing"]:
            return "communication"
        else:
            return "general"
    
    def _calculate_skill_improvements(self, employee: Employee) -> Dict[str, float]:
        return {skill.name: skill.progress_rate for skill in employee.skills}
    
    def _save_feedback(self, feedback: Feedback):
        """フィードバックをファイルに保存"""
        feedback_path = self.data_dir / "feedbacks" / f"{feedback.id}.json"
        with open(feedback_path, "w", encoding="utf-8") as f:
            json.dump(feedback.dict(), f, ensure_ascii=False, indent=2)
    
    def _define_growth_objectives(self, employee: Employee, analysis: Dict[str, Any]) -> List[str]:
        objectives = []
        for skill in employee.skills:
            if skill.progress_rate < 70:
                objectives.append(f"Improve {skill.name} to intermediate level")
        return objectives[:5]  # Top 5 objectives
    
    def _create_milestones(self, employee: Employee, timeframe: int) -> List[Dict[str, Any]]:
        milestones = []
        intervals = timeframe // 3
        
        for i in range(3):
            milestone = {
                "name": f"Month {i+1} Review",
                "date": (datetime.now() + timedelta(days=intervals * (i+1))).isoformat(),
                "goals": self._define_milestone_goals(employee, i+1)
            }
            milestones.append(milestone)
        
        return milestones
    
    def _define_milestone_goals(self, employee: Employee, month: int) -> List[str]:
        if month == 1:
            return ["Complete foundational training", "Establish routine"]
        elif month == 2:
            return ["Apply learned skills", "Receive peer feedback"]
        else:
            return ["Demonstrate independence", "Mentor others"]
    
    def _design_learning_path(self, employee: Employee) -> List[Dict[str, Any]]:
        path = []
        for skill in employee.skills:
            if skill.progress_rate < 70:
                path.append({
                    "skill": skill.name,
                    "current_level": skill.level.value,
                    "target_level": "intermediate",
                    "recommended_resources": ["Online course", "Mentorship", "Practice projects"]
                })
        return path
    
    def _identify_support_mechanisms(self, employee: Employee) -> List[str]:
        mechanisms = ["Regular 1-on-1 meetings", "Peer learning sessions"]
        if employee.learning_pace < 1.0:
            mechanisms.append("Additional tutoring")
        return mechanisms
    
    def _define_success_metrics(self, employee: Employee) -> Dict[str, Any]:
        return {
            "skill_improvement": "20% increase in skill levels",
            "project_completion": "Successfully complete 3 projects",
            "feedback_score": "Achieve 4+ rating in peer reviews"
        }
    
    def _create_review_schedule(self, timeframe: int) -> List[Dict[str, str]]:
        schedule = []
        for week in range(0, timeframe, 14):  # Bi-weekly reviews
            schedule.append({
                "date": (datetime.now() + timedelta(days=week)).isoformat(),
                "type": "Progress Review",
                "duration": "30 minutes"
            })
        return schedule
    
    def _calculate_skill_progress(self, employee: Employee, start_date: datetime, 
                                 end_date: datetime) -> List[SkillProgress]:
        progress_list = []
        for skill in employee.skills:
            progress = SkillProgress(
                skill_name=skill.name,
                initial_level=50.0,  # Placeholder
                current_level=skill.progress_rate,
                target_level=100.0,
                progress_percentage=skill.progress_rate,
                last_assessment_date=datetime.now(),
                improvement_rate=2.5  # Placeholder
            )
            progress_list.append(progress)
        return progress_list
    
    def _determine_growth_trend(self, skill_progress: List[SkillProgress]) -> GrowthTrend:
        avg_improvement = sum(sp.improvement_rate for sp in skill_progress) / len(skill_progress) if skill_progress else 0
        
        if avg_improvement > 5:
            return GrowthTrend.RAPID
        elif avg_improvement > 2:
            return GrowthTrend.STEADY
        elif avg_improvement > 0:
            return GrowthTrend.SLOW
        else:
            return GrowthTrend.STAGNANT
    
    def _check_milestones(self, employee: Employee, start_date: datetime, 
                         end_date: datetime) -> List[Milestone]:
        # Placeholder implementation
        return []
    
    def _identify_achievements(self, employee: Employee, start_date: datetime, 
                              end_date: datetime) -> List[str]:
        achievements = []
        for skill in employee.skills:
            if skill.progress_rate > 80:
                achievements.append(f"Mastered {skill.name}")
        return achievements
    
    def _identify_challenges(self, employee: Employee) -> List[str]:
        return employee.improvement_areas[:3]
    
    def _extract_lessons_learned(self, employee: Employee) -> List[str]:
        return ["Importance of consistent practice", "Value of peer feedback"]
    
    def _calculate_feedback_implementation_rate(self, employee: Employee) -> float:
        return 75.0  # Placeholder
    
    def _predict_growth_rate(self, employee: Employee) -> float:
        return employee.learning_pace * 2.5
    
    def _recommend_focus_areas(self, employee: Employee) -> List[str]:
        areas = []
        for skill in employee.skills:
            if skill.progress_rate < 60:
                areas.append(skill.name)
        return areas[:3]
    
    def _identify_risk_indicators(self, employee: Employee) -> List[str]:
        return self._identify_risk_factors(employee)
    
    def _provide_skill_support(self, employee: Employee) -> List[str]:
        return [
            "Identify specific skill gaps",
            "Recommend targeted learning resources",
            "Pair with skilled mentor",
            "Create practice opportunities"
        ]
    
    def _provide_motivation_support(self, employee: Employee) -> List[str]:
        return [
            "Acknowledge recent achievements",
            "Set achievable short-term goals",
            "Share success stories from peers",
            "Offer flexible learning options"
        ]
    
    def _provide_communication_support(self, employee: Employee) -> List[str]:
        return [
            "Practice active listening techniques",
            "Provide communication templates",
            "Arrange mock presentation sessions",
            "Encourage team collaboration"
        ]
    
    def _provide_workload_support(self, employee: Employee) -> List[str]:
        return [
            "Review current task priorities",
            "Teach time management techniques",
            "Identify tasks for delegation",
            "Establish realistic deadlines"
        ]
    
    def _provide_general_support(self, employee: Employee) -> List[str]:
        return [
            "Schedule regular check-ins",
            "Provide comprehensive resources",
            "Connect with support network",
            "Monitor progress closely"
        ]
    
    def _generate_follow_up_actions(self, employee: Employee, issue_type: str) -> List[str]:
        return [
            f"Review progress in 1 week",
            f"Adjust support based on {issue_type} resolution",
            "Gather feedback on support effectiveness"
        ]
    
    def _recommend_resources(self, employee: Employee, issue_type: str) -> List[Dict[str, str]]:
        resources = []
        if issue_type == "skill_gap":
            resources.append({
                "type": "Online Course",
                "title": "Advanced Skills Training",
                "url": "https://example.com/training"
            })
        resources.append({
            "type": "Article",
            "title": f"Overcoming {issue_type} Challenges",
            "url": "https://example.com/article"
        })
        return resources
    
    def load_employee(self, employee_id: str) -> Optional[Employee]:
        """社員データを読み込み"""
        employee_path = self.data_dir / "employees" / f"{employee_id}.json"
        if employee_path.exists():
            with open(employee_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Employee(**data)
        return None
    
    def save_employee(self, employee: Employee):
        """社員データを保存"""
        employee_path = self.data_dir / "employees" / f"{employee.id}.json"
        with open(employee_path, "w", encoding="utf-8") as f:
            json.dump(employee.dict(), f, ensure_ascii=False, indent=2)
from typing import List, Dict, Any
from datetime import datetime, timedelta

from ..models import Employee, Feedback, FeedbackType, Priority, ActionItem


class FeedbackService:
    """フィードバック生成・管理サービス"""
    
    def generate_personalized_feedback(self, employee: Employee, context: Dict[str, Any]) -> Dict[str, Any]:
        """個人に合わせたフィードバックを生成"""
        feedback_style = self._determine_feedback_style(employee)
        content = self._create_feedback_content(employee, context, feedback_style)
        
        return {
            "style": feedback_style,
            "content": content,
            "delivery_method": self._recommend_delivery_method(employee),
            "timing": self._suggest_optimal_timing(employee)
        }
    
    def create_action_plan(self, employee: Employee, feedback_analysis: Dict[str, Any]) -> List[ActionItem]:
        """具体的なアクションプランを作成"""
        action_items = []
        
        # 改善が必要なスキルに対するアクション
        weak_skills = [s for s in employee.skills if s.progress_rate < 50]
        for skill in weak_skills[:3]:  # 上位3つに絞る
            action_items.append(ActionItem(
                description=f"Improve {skill.name} through targeted practice",
                due_date=datetime.now() + timedelta(days=30),
                priority=Priority.HIGH if skill.progress_rate < 30 else Priority.MEDIUM,
                resources=self._get_skill_resources(skill.name),
                estimated_hours=20.0
            ))
        
        # 目標に対するアクション
        if not employee.current_objectives:
            action_items.append(ActionItem(
                description="Set clear learning objectives for the next month",
                due_date=datetime.now() + timedelta(days=7),
                priority=Priority.HIGH,
                resources=["Goal setting template", "Career development guide"],
                estimated_hours=2.0
            ))
        
        return action_items
    
    def adjust_communication_style(self, employee: Employee, base_message: str) -> str:
        """コミュニケーションスタイルを調整"""
        if employee.learning_pace < 0.7:
            # ゆっくり学習する人には丁寧で段階的な説明
            return self._make_supportive_tone(base_message)
        elif employee.learning_pace > 1.3:
            # 速く学習する人には簡潔で直接的な説明
            return self._make_direct_tone(base_message)
        else:
            # 標準的な学習ペースの人にはバランスの取れた説明
            return self._make_balanced_tone(base_message)
    
    def generate_encouragement(self, employee: Employee) -> str:
        """個人に合わせた励ましのメッセージを生成"""
        strengths = employee.strengths
        recent_achievements = self._identify_recent_achievements(employee)
        
        if strengths:
            strength_message = f"Your {strengths[0]} continues to be a valuable asset."
        else:
            strength_message = "You're showing consistent effort in your development."
        
        if recent_achievements:
            achievement_message = f" Your recent progress in {recent_achievements[0]} is commendable."
        else:
            achievement_message = " Keep up the steady progress!"
        
        return strength_message + achievement_message
    
    def suggest_feedback_frequency(self, employee: Employee) -> Dict[str, Any]:
        """フィードバック頻度を提案"""
        # 学習ペースと現在のパフォーマンスに基づいて頻度を調整
        if employee.learning_pace < 0.6 or len(employee.improvement_areas) > 4:
            frequency = "weekly"
            reasoning = "Frequent check-ins will help maintain momentum"
        elif employee.learning_pace > 1.2 and len(employee.improvement_areas) < 2:
            frequency = "monthly"
            reasoning = "Self-directed learning with periodic reviews"
        else:
            frequency = "bi-weekly"
            reasoning = "Regular support with room for independence"
        
        return {
            "recommended_frequency": frequency,
            "reasoning": reasoning,
            "next_review_date": self._calculate_next_review_date(frequency)
        }
    
    def _determine_feedback_style(self, employee: Employee) -> str:
        """フィードバックスタイルを決定"""
        if employee.learning_pace < 0.7:
            return "supportive_detailed"
        elif employee.overall_rating and employee.overall_rating > 4.0:
            return "challenging_growth"
        elif len(employee.improvement_areas) > 3:
            return "structured_guidance"
        else:
            return "balanced_encouragement"
    
    def _create_feedback_content(self, employee: Employee, context: Dict[str, Any], style: str) -> Dict[str, str]:
        """スタイルに応じたフィードバック内容を作成"""
        if style == "supportive_detailed":
            return {
                "opening": f"Hi {employee.name}, I want to recognize your dedication to learning.",
                "main_message": "Let's work together to break down your goals into manageable steps.",
                "specific_guidance": "I've identified specific areas where we can focus your efforts.",
                "closing": "Remember, progress takes time, and you're doing great!"
            }
        elif style == "challenging_growth":
            return {
                "opening": f"{employee.name}, your strong performance opens up new opportunities.",
                "main_message": "I'd like to challenge you with some advanced objectives.",
                "specific_guidance": "Here are areas where you can push your limits.",
                "closing": "I'm confident you can reach the next level!"
            }
        elif style == "structured_guidance":
            return {
                "opening": f"Hello {employee.name}, let's focus on creating a clear path forward.",
                "main_message": "I've prioritized your development areas based on impact.",
                "specific_guidance": "Following this structured approach will maximize your progress.",
                "closing": "Consistency in these areas will lead to significant improvement."
            }
        else:  # balanced_encouragement
            return {
                "opening": f"Hi {employee.name}, you're making steady progress!",
                "main_message": "Let's build on your strengths while addressing key growth areas.",
                "specific_guidance": "I have some targeted suggestions for your development.",
                "closing": "Keep up the excellent work!"
            }
    
    def _recommend_delivery_method(self, employee: Employee) -> str:
        """フィードバック提供方法を推奨"""
        if employee.preferred_learning_style == "visual":
            return "written_with_diagrams"
        elif employee.preferred_learning_style == "auditory":
            return "verbal_discussion"
        elif employee.preferred_learning_style == "kinesthetic":
            return "hands_on_demonstration"
        else:
            return "combined_approach"
    
    def _suggest_optimal_timing(self, employee: Employee) -> str:
        """最適なタイミングを提案"""
        if employee.learning_pace < 0.7:
            return "end_of_week"  # ストレスの少ない時間
        else:
            return "beginning_of_week"  # 行動計画を立てやすい時間
    
    def _get_skill_resources(self, skill_name: str) -> List[str]:
        """スキル別のリソースを取得"""
        resource_map = {
            "communication": ["Public speaking course", "Writing workshop", "Active listening guide"],
            "programming": ["Coding practice platform", "Technical documentation", "Code review sessions"],
            "project_management": ["PM certification course", "Project planning templates", "Agile methodology guide"],
            "leadership": ["Leadership development program", "Mentoring guide", "Team building exercises"]
        }
        
        # キーワードマッチングで適切なリソースを選択
        for key, resources in resource_map.items():
            if key.lower() in skill_name.lower():
                return resources
        
        return ["Online course", "Practice exercises", "Mentorship session"]
    
    def _make_supportive_tone(self, message: str) -> str:
        """サポート的なトーンに調整"""
        supportive_phrases = [
            "I understand this can be challenging, and that's completely normal.",
            "Let's take this step by step.",
            "You're making progress, even if it doesn't always feel that way."
        ]
        return f"{supportive_phrases[0]} {message}"
    
    def _make_direct_tone(self, message: str) -> str:
        """直接的なトーンに調整"""
        return f"Here's what you need to focus on: {message}"
    
    def _make_balanced_tone(self, message: str) -> str:
        """バランスの取れたトーンに調整"""
        return f"You're doing well overall. {message} This will help you continue growing."
    
    def _identify_recent_achievements(self, employee: Employee) -> List[str]:
        """最近の成果を特定"""
        achievements = []
        
        # 高い進捗率のスキルを成果として認識
        for skill in employee.skills:
            if skill.progress_rate > 70:
                achievements.append(skill.name)
        
        # 完了したトレーニングも成果として認識
        if employee.completed_trainings:
            achievements.extend(employee.completed_trainings[-2:])  # 最新2つ
        
        return achievements[:3]  # 上位3つまで
    
    def _calculate_next_review_date(self, frequency: str) -> str:
        """次のレビュー日を計算"""
        now = datetime.now()
        if frequency == "weekly":
            next_date = now + timedelta(weeks=1)
        elif frequency == "bi-weekly":
            next_date = now + timedelta(weeks=2)
        elif frequency == "monthly":
            next_date = now + timedelta(weeks=4)
        else:
            next_date = now + timedelta(weeks=2)  # デフォルト
        
        return next_date.isoformat()
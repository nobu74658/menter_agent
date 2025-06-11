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
            strength_message = f"あなたの「{strengths[0]}」は引き続き貴重な資質です。"
        else:
            strength_message = "あなたは成長に向けて継続的な努力を示しています。"
        
        if recent_achievements:
            achievement_message = f"{recent_achievements[0]}での最近の進歩は素晴らしいものです。"
        else:
            achievement_message = "この調子で着実に進歩を続けてください！"
        
        return strength_message + achievement_message
    
    def suggest_feedback_frequency(self, employee: Employee) -> Dict[str, Any]:
        """フィードバック頻度を提案"""
        # 学習ペースと現在のパフォーマンスに基づいて頻度を調整
        if employee.learning_pace < 0.6 or len(employee.improvement_areas) > 4:
            frequency = "weekly"
            reasoning = "頻繁なチェックインが継続的な成長を支援します"
        elif employee.learning_pace > 1.2 and len(employee.improvement_areas) < 2:
            frequency = "monthly"
            reasoning = "自律的な学習と定期的なレビューが適しています"
        else:
            frequency = "bi-weekly"
            reasoning = "独立性を保ちつつ定期的なサポートを提供します"
        
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
                "opening": f"{employee.name}さん、学習への献身的な取り組みを評価しています。",
                "main_message": "目標を達成可能なステップに分けて、一緒に取り組んでいきましょう。",
                "specific_guidance": "あなたの努力を集中させるべき具体的な領域を特定しました。",
                "closing": "成長には時間がかかることを覚えておいてください。あなたは素晴らしい取り組みをしています！"
            }
        elif style == "challenging_growth":
            return {
                "opening": f"{employee.name}さん、あなたの優れたパフォーマンスが新たな機会を開いています。",
                "main_message": "より高度な目標に挑戦していただきたいと思います。",
                "specific_guidance": "あなたの限界を押し広げることができる領域をご紹介します。",
                "closing": "あなたなら次のレベルに到達できると確信しています！"
            }
        elif style == "structured_guidance":
            return {
                "opening": f"{employee.name}さん、明確な前進の道筋を作ることに焦点を当てましょう。",
                "main_message": "影響度に基づいて開発領域の優先順位を付けました。",
                "specific_guidance": "この構造化されたアプローチに従うことで、進歩が最大化されます。",
                "closing": "これらの領域での一貫性が大幅な改善につながります。"
            }
        else:  # balanced_encouragement
            return {
                "opening": f"{employee.name}さん、着実な進歩を続けています！",
                "main_message": "強みを活かしながら、重要な成長領域に取り組んでいきましょう。",
                "specific_guidance": "あなたの成長のための具体的な提案があります。",
                "closing": "この調子で素晴らしい取り組みを続けてください！"
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
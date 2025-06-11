from typing import List, Dict, Any, Optional
from datetime import datetime
import random

from ..models import Employee, Feedback, FeedbackType, Priority


class FeedbackService:
    """フィードバック生成サービス"""
    
    def __init__(self):
        self.feedback_templates = self._load_feedback_templates()
    
    def generate_strength_feedback(self, employee: Employee) -> Dict[str, Any]:
        """強みに関するフィードバックを生成"""
        if not employee.strengths:
            return {
                "type": "general",
                "message": "Continue to develop and identify your unique strengths."
            }
        
        strength_feedback = {
            "type": "strength_recognition",
            "highlights": employee.strengths[:3],
            "message": self._create_strength_message(employee.strengths),
            "recommendations": self._suggest_strength_leverage(employee.strengths)
        }
        
        return strength_feedback
    
    def generate_improvement_feedback(self, employee: Employee) -> Dict[str, Any]:
        """改善点に関するフィードバックを生成"""
        if not employee.improvement_areas:
            return {
                "type": "general",
                "message": "Keep pushing yourself to new challenges."
            }
        
        improvement_feedback = {
            "type": "constructive",
            "focus_areas": employee.improvement_areas[:3],
            "message": self._create_improvement_message(employee.improvement_areas),
            "action_plan": self._create_improvement_plan(employee.improvement_areas),
            "resources": self._suggest_resources(employee.improvement_areas)
        }
        
        return improvement_feedback
    
    def generate_contextual_feedback(self, employee: Employee, context: str) -> Dict[str, Any]:
        """状況に応じたフィードバックを生成"""
        feedback_map = {
            "project_completion": self._generate_project_feedback,
            "skill_assessment": self._generate_skill_feedback,
            "team_collaboration": self._generate_team_feedback,
            "deadline_miss": self._generate_deadline_feedback,
            "innovation": self._generate_innovation_feedback
        }
        
        generator = feedback_map.get(context, self._generate_general_feedback)
        return generator(employee)
    
    def personalize_feedback_tone(self, feedback: str, employee: Employee) -> str:
        """社員の特性に合わせてフィードバックのトーンを調整"""
        
        # 学習ペースに基づく調整
        if employee.learning_pace < 0.8:
            # より励ましのトーン
            feedback = feedback.replace("should", "could consider")
            feedback = feedback.replace("need to", "might benefit from")
            feedback = f"Take your time. {feedback}"
        elif employee.learning_pace > 1.5:
            # よりチャレンジングなトーン
            feedback = feedback.replace("could", "should")
            feedback = f"{feedback} Given your rapid progress, consider taking on additional challenges."
        
        # 学習スタイルに基づく調整
        if employee.preferred_learning_style == "visual":
            feedback += " Visual aids and diagrams might help reinforce these concepts."
        elif employee.preferred_learning_style == "hands-on":
            feedback += " Practice these concepts through real projects for better retention."
        
        return feedback
    
    def create_feedback_summary(self, feedbacks: List[Feedback]) -> Dict[str, Any]:
        """複数のフィードバックからサマリーを作成"""
        if not feedbacks:
            return {"status": "no_feedback_available"}
        
        summary = {
            "total_feedbacks": len(feedbacks),
            "feedback_types": self._count_feedback_types(feedbacks),
            "common_themes": self._identify_common_themes(feedbacks),
            "average_impact_score": self._calculate_average_impact(feedbacks),
            "action_items_pending": self._count_pending_actions(feedbacks),
            "key_recommendations": self._extract_key_recommendations(feedbacks)
        }
        
        return summary
    
    def _load_feedback_templates(self) -> Dict[str, List[str]]:
        """フィードバックテンプレートを読み込み"""
        return {
            "positive": [
                "Excellent work on {achievement}. Your {strength} really made a difference.",
                "Your progress in {area} has been remarkable. Keep up the great work!",
                "You've shown exceptional {quality} in your recent work."
            ],
            "constructive": [
                "To further develop {skill}, consider {action}.",
                "I noticed some challenges with {area}. Let's work on {solution}.",
                "Your {area} could benefit from {improvement}."
            ],
            "developmental": [
                "For your next growth phase, focus on {objective}.",
                "To reach the next level, developing {skill} will be crucial.",
                "Consider expanding your expertise in {area}."
            ]
        }
    
    def _create_strength_message(self, strengths: List[str]) -> str:
        """強みメッセージを作成"""
        if len(strengths) == 1:
            return f"Your {strengths[0]} is a significant asset to the team."
        elif len(strengths) == 2:
            return f"Your {strengths[0]} and {strengths[1]} are valuable strengths."
        else:
            return f"Your key strengths include {', '.join(strengths[:2])}, and {strengths[2]}."
    
    def _suggest_strength_leverage(self, strengths: List[str]) -> List[str]:
        """強みを活かす方法を提案"""
        suggestions = []
        for strength in strengths[:3]:
            if "communication" in strength.lower():
                suggestions.append("Consider leading team presentations or client meetings")
            elif "technical" in strength.lower():
                suggestions.append("Mentor junior developers on technical topics")
            elif "problem" in strength.lower():
                suggestions.append("Take ownership of complex problem-solving tasks")
            else:
                suggestions.append(f"Find opportunities to apply your {strength} in new projects")
        
        return suggestions
    
    def _create_improvement_message(self, areas: List[str]) -> str:
        """改善メッセージを作成"""
        primary_area = areas[0]
        return f"Focusing on {primary_area} will significantly enhance your overall performance. " \
               f"This is a common growth area that many successful professionals have worked through."
    
    def _create_improvement_plan(self, areas: List[str]) -> List[Dict[str, str]]:
        """改善計画を作成"""
        plan = []
        for area in areas[:3]:
            plan.append({
                "area": area,
                "short_term": f"Week 1-2: Understand the basics of {area}",
                "medium_term": f"Week 3-4: Practice {area} in controlled settings",
                "long_term": f"Month 2+: Apply {area} in real projects"
            })
        return plan
    
    def _suggest_resources(self, areas: List[str]) -> List[Dict[str, str]]:
        """リソースを提案"""
        resources = []
        for area in areas[:2]:
            resources.extend([
                {
                    "type": "course",
                    "title": f"Mastering {area}",
                    "format": "online"
                },
                {
                    "type": "book",
                    "title": f"The Complete Guide to {area}",
                    "format": "digital/physical"
                }
            ])
        return resources
    
    def _generate_project_feedback(self, employee: Employee) -> Dict[str, Any]:
        """プロジェクト完了フィードバック"""
        return {
            "type": "project_completion",
            "message": "Congratulations on completing the project!",
            "strengths_demonstrated": random.sample(employee.strengths, min(2, len(employee.strengths))) if employee.strengths else [],
            "lessons_learned": ["Time management", "Team coordination", "Technical implementation"],
            "next_steps": ["Apply learnings to next project", "Share knowledge with team"]
        }
    
    def _generate_skill_feedback(self, employee: Employee) -> Dict[str, Any]:
        """スキル評価フィードバック"""
        improving_skills = [s.name for s in employee.skills if 40 < s.progress_rate < 70]
        strong_skills = [s.name for s in employee.skills if s.progress_rate >= 70]
        
        return {
            "type": "skill_assessment",
            "strong_skills": strong_skills,
            "improving_skills": improving_skills,
            "focus_recommendation": improving_skills[0] if improving_skills else "Continue balanced development"
        }
    
    def _generate_team_feedback(self, employee: Employee) -> Dict[str, Any]:
        """チーム協力フィードバック"""
        return {
            "type": "team_collaboration",
            "collaboration_score": random.randint(70, 95),
            "positive_behaviors": ["Active participation", "Supportive attitude", "Clear communication"],
            "enhancement_areas": ["Cross-functional collaboration", "Conflict resolution"]
        }
    
    def _generate_deadline_feedback(self, employee: Employee) -> Dict[str, Any]:
        """締切遅延フィードバック"""
        return {
            "type": "deadline_miss",
            "message": "Let's discuss the challenges you faced with the recent deadline.",
            "root_causes": ["Time estimation", "Task prioritization", "Resource planning"],
            "prevention_strategies": [
                "Break down tasks into smaller milestones",
                "Regular progress check-ins",
                "Early escalation of blockers"
            ]
        }
    
    def _generate_innovation_feedback(self, employee: Employee) -> Dict[str, Any]:
        """イノベーションフィードバック"""
        return {
            "type": "innovation",
            "message": "Your innovative approach shows great initiative!",
            "innovation_aspects": ["Creative problem-solving", "New perspective", "Risk-taking"],
            "encouragement": "Continue exploring new ideas while balancing with execution"
        }
    
    def _generate_general_feedback(self, employee: Employee) -> Dict[str, Any]:
        """一般的なフィードバック"""
        return {
            "type": "general",
            "message": f"Keep up the good work, {employee.name}!",
            "overall_performance": "satisfactory",
            "continue_doing": employee.strengths[:2] if employee.strengths else ["Current efforts"],
            "consider_improving": employee.improvement_areas[:2] if employee.improvement_areas else ["Seek new challenges"]
        }
    
    def _count_feedback_types(self, feedbacks: List[Feedback]) -> Dict[str, int]:
        """フィードバックタイプをカウント"""
        type_counts = {}
        for feedback in feedbacks:
            type_counts[feedback.type.value] = type_counts.get(feedback.type.value, 0) + 1
        return type_counts
    
    def _identify_common_themes(self, feedbacks: List[Feedback]) -> List[str]:
        """共通テーマを特定"""
        themes = []
        categories = {}
        
        for feedback in feedbacks:
            categories[feedback.category] = categories.get(feedback.category, 0) + 1
        
        # 最も頻繁なカテゴリーをテーマとして返す
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        return [cat[0] for cat in sorted_categories[:3]]
    
    def _calculate_average_impact(self, feedbacks: List[Feedback]) -> float:
        """平均インパクトスコアを計算"""
        if not feedbacks:
            return 0.0
        
        total_impact = sum(f.impact_score for f in feedbacks)
        return round(total_impact / len(feedbacks), 2)
    
    def _count_pending_actions(self, feedbacks: List[Feedback]) -> int:
        """保留中のアクションアイテムをカウント"""
        pending_count = 0
        for feedback in feedbacks:
            pending_count += sum(1 for action in feedback.action_items if not action.completed)
        return pending_count
    
    def _extract_key_recommendations(self, feedbacks: List[Feedback]) -> List[str]:
        """主要な推奨事項を抽出"""
        all_recommendations = []
        for feedback in feedbacks:
            all_recommendations.extend(feedback.recommendations)
        
        # 重複を除いて最初の5つを返す
        unique_recommendations = list(dict.fromkeys(all_recommendations))
        return unique_recommendations[:5]
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import json
from pathlib import Path


def safe_json_dumps(obj, **kwargs):
    """datetime対応のJSONシリアライザー"""
    def default_serializer(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")
    
    return json.dumps(obj, default=default_serializer, **kwargs)

from .base import BaseMentorAgent
from ..models import (
    Employee, Feedback, GrowthRecord, 
    FeedbackType, Priority, ActionItem,
    SkillProgress, Milestone, MilestoneStatus,
    GrowthTrend
)
from ..services.llm_service import LLMService
from ..services.autonomous_agent_service import AutonomousAgentService
from ..services.knowledge_search_service import KnowledgeSearchService
from ..services.task_planner_service import TaskPlannerService


class MentorAgent(BaseMentorAgent):
    """メンターエージェントの実装"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.llm_service = LLMService()
        self.use_llm = config.get('use_llm', True) if config else True
        
        # 自律的エージェント機能の初期化
        self.autonomous_agent = AutonomousAgentService()
        self.knowledge_search = KnowledgeSearchService()
        self.task_planner = TaskPlannerService()
        
        # 自律モードの設定
        self.autonomous_mode = config.get('autonomous_mode', True) if config else True
        self.auto_search = config.get('auto_search', True) if config else True
        
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
        """個別化されたフィードバックを生成（LLM + ルールベースハイブリッド）"""
        # 分析結果を取得
        analysis = self.analyze_employee(employee)
        
        # フィードバックタイプの決定
        feedback_type = self._determine_feedback_type(analysis)
        
        # LLMを使用してフィードバック生成を試行
        llm_content = None
        if self.use_llm and self.llm_service.is_available():
            try:
                llm_content = self.llm_service.generate_personalized_feedback(
                    employee, analysis, feedback_type
                )
                if llm_content:
                    self.logger.info(f"Generated LLM feedback for {employee.name}")
            except Exception as e:
                self.logger.warning(f"LLM feedback generation failed, falling back to rule-based: {e}")
        
        # フィードバック内容の生成（LLMまたはルールベース）
        if llm_content:
            feedback_content = self._format_llm_feedback_content(llm_content, employee, analysis)
        else:
            feedback_content = self._create_feedback_content(employee, analysis, feedback_type)
        
        # 推奨事項の生成（LLMを優先、フォールバックでルールベース）
        recommendations = self._generate_enhanced_recommendations(employee, analysis)
        
        # アクションアイテムの生成
        action_items = self._generate_action_items(employee, analysis)
        
        feedback = Feedback(
            id=str(uuid.uuid4()),
            employee_id=employee.id,
            mentor_id="mentor_agent_llm" if llm_content else "mentor_agent_rule",
            type=feedback_type,
            category=self._determine_feedback_category(employee),
            summary=feedback_content["summary"],
            detailed_feedback=feedback_content["detailed"],
            impact_score=feedback_content["impact_score"],
            confidence_level=0.95 if llm_content else 0.85,
            specific_examples=feedback_content["examples"],
            observed_behaviors=feedback_content["behaviors"],
            recommendations=recommendations,
            action_items=action_items,
            skill_improvements=self._calculate_skill_improvements(employee),
            expected_timeline="30-60 days",
            follow_up_required=len(action_items) > 0,
            is_automated=True
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
        """状況に応じたサポートを提供（LLM強化）"""
        support_response = {
            "employee_id": employee.id,
            "issue_type": issue_type,
            "timestamp": datetime.now().isoformat(),
            "support_provided": [],
            "support_message": ""
        }
        
        # LLMを使用したサポートメッセージ生成を試行
        if self.use_llm and self.llm_service.is_available():
            try:
                llm_message = self.llm_service.generate_support_message(employee, issue_type)
                if llm_message:
                    support_response["support_message"] = llm_message
                    support_response["message_source"] = "llm"
                    self.logger.info(f"Generated LLM support message for {employee.name}, issue: {issue_type}")
            except Exception as e:
                self.logger.warning(f"LLM support message generation failed: {e}")
        
        # ルールベースのサポートアクション（従来の機能を維持）
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
            risks.append("学習ペースが著しく遅い状況です")
        if len(employee.improvement_areas) > 5:
            risks.append("改善が必要な領域が多数あります")
        if not employee.current_objectives:
            risks.append("明確な目標が設定されていません")
        return risks
    
    def _generate_recommendations(self, employee: Employee) -> List[str]:
        recommendations = []
        for area in employee.improvement_areas[:3]:  # Top 3 areas
            recommendations.append(f"{area}の向上に重点的に取り組みましょう")
        if employee.learning_pace < 1.0:
            recommendations.append("学習アプローチの調整を検討してください")
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
        # 総合評価の日本語変換
        assessment_map = {
            "Excellent": "優秀",
            "Good": "良好", 
            "Satisfactory": "普通",
            "Needs Improvement": "要改善"
        }
        trajectory_map = {
            "Accelerated": "加速的",
            "Normal": "標準的",
            "Slow": "緩やか"
        }
        
        assessment_jp = assessment_map.get(analysis['overall_assessment'], analysis['overall_assessment'])
        trajectory_jp = trajectory_map.get(analysis['growth_trajectory'], analysis['growth_trajectory'])
        
        return {
            "summary": f"{employee.name}さんへのフィードバック",
            "detailed": f"分析の結果、あなたの総合的なパフォーマンスは「{assessment_jp}」です。"
                       f"成長の軌道は「{trajectory_jp}」と評価されます。",
            "impact_score": self.calculate_growth_score(employee),
            "examples": [f"{s.name}で進歩を示しています" for s in employee.skills if s.progress_rate > 70],
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
            # Pydanticバージョン互換性のためjson.dumpを使用
            if hasattr(feedback, 'model_dump'):
                # Pydantic v2
                data = feedback.model_dump()
            else:
                # Pydantic v1
                data = feedback.dict()
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    def _define_growth_objectives(self, employee: Employee, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        objectives = []
        for skill in employee.skills:
            if skill.progress_rate < 70:
                objectives.append({
                    "area": skill.name,
                    "current_state": skill.level.value,
                    "target_state": "intermediate",
                    "priority": "high" if skill.progress_rate < 40 else "medium"
                })
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
        for idx, skill in enumerate(employee.skills):
            if skill.progress_rate < 70:
                path.append({
                    "step": idx + 1,
                    "skill": skill.name,
                    "current_level": skill.level.value,
                    "target_level": "intermediate",
                    "duration_days": 30,
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
                achievements.append(f"{skill.name}をマスターしました")
        return achievements
    
    def _identify_challenges(self, employee: Employee) -> List[str]:
        return employee.improvement_areas[:3]
    
    def _extract_lessons_learned(self, employee: Employee) -> List[str]:
        return ["継続的な練習の重要性", "同僚からのフィードバックの価値"]
    
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
            "具体的なスキルギャップを特定しました",
            "対象となる学習リソースを推奨します",
            "経験豊富なメンターとのマッチングを手配します",
            "実践的な練習機会を提供します"
        ]
    
    def _provide_motivation_support(self, employee: Employee) -> List[str]:
        return [
            "最近の成果を認識し、評価しています",
            "達成可能な短期目標を設定します",
            "同僚の成功事例を共有します",
            "柔軟な学習オプションを提供します"
        ]
    
    def _provide_communication_support(self, employee: Employee) -> List[str]:
        return [
            "アクティブリスニング技術の練習を行います",
            "コミュニケーションテンプレートを提供します",
            "模擬プレゼンテーションセッションを手配します",
            "チームコラボレーションを促進します"
        ]
    
    def _provide_workload_support(self, employee: Employee) -> List[str]:
        return [
            "現在のタスクの優先順位を見直します",
            "時間管理技術を指導します",
            "委任可能なタスクを特定します",
            "現実的な期限を設定します"
        ]
    
    def _provide_general_support(self, employee: Employee) -> List[str]:
        return [
            "定期的なチェックインをスケジュールします",
            "包括的なリソースを提供します",
            "サポートネットワークとの接続を支援します",
            "進捗を細かく監視します"
        ]
    
    def _generate_follow_up_actions(self, employee: Employee, issue_type: str) -> List[str]:
        issue_type_jp = {
            "skill_gap": "スキルギャップ",
            "motivation": "モチベーション",
            "communication": "コミュニケーション",
            "workload": "作業負荷"
        }.get(issue_type, issue_type)
        
        return [
            "1週間後に進捗を確認します",
            f"{issue_type_jp}の解決状況に基づいてサポートを調整します",
            "サポートの効果について フィードバックを収集します"
        ]
    
    def _recommend_resources(self, employee: Employee, issue_type: str) -> List[Dict[str, str]]:
        resources = []
        issue_type_jp = {
            "skill_gap": "スキルギャップ",
            "motivation": "モチベーション",
            "communication": "コミュニケーション",
            "workload": "作業負荷"
        }.get(issue_type, issue_type)
        
        if issue_type == "skill_gap":
            resources.append({
                "type": "オンラインコース",
                "title": "高度スキル研修プログラム",
                "url": "https://example.com/training"
            })
        resources.append({
            "type": "記事",
            "title": f"{issue_type_jp}課題克服ガイド",
            "url": "https://example.com/article"
        })
        return resources
    
    # LLM統合用ヘルパーメソッド
    def _format_llm_feedback_content(
        self, 
        llm_content: Dict[str, str], 
        employee: Employee, 
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """LLMが生成したフィードバック内容をフォーマット"""
        return {
            "summary": llm_content.get("summary", f"{employee.name}さんへのフィードバック"),
            "detailed": llm_content.get("detailed", "詳細な分析に基づくフィードバックです。"),
            "impact_score": self.calculate_growth_score(employee),
            "examples": [f"{s.name}で進歩を示しています" for s in employee.skills if s.progress_rate > 70],
            "behaviors": employee.strengths[:3],
            "recommendations": [llm_content.get("next_steps", "継続的な努力を続けてください。")],
            "encouragement": llm_content.get("encouragement", "")
        }
    
    def _generate_enhanced_recommendations(self, employee: Employee, analysis: Dict[str, Any]) -> List[str]:
        """LLMと ルールベースを組み合わせた推奨事項生成"""
        recommendations = []
        
        # LLMによる推奨事項生成を試行
        if self.use_llm and self.llm_service.is_available():
            try:
                llm_recommendations = self.llm_service.generate_growth_recommendations(employee, analysis)
                if llm_recommendations:
                    recommendations.extend(llm_recommendations)
                    self.logger.info(f"Generated {len(llm_recommendations)} LLM recommendations for {employee.name}")
            except Exception as e:
                self.logger.warning(f"LLM recommendations generation failed: {e}")
        
        # LLMが利用できない場合や不十分な場合はルールベースを使用
        if len(recommendations) < 3:
            rule_based_recommendations = self._generate_recommendations(employee)
            recommendations.extend(rule_based_recommendations)
        
        # 重複を除去し、最大5つに制限
        unique_recommendations = []
        seen = set()
        for rec in recommendations:
            if rec not in seen:
                unique_recommendations.append(rec)
                seen.add(rec)
                if len(unique_recommendations) >= 5:
                    break
        
        return unique_recommendations
    
    def toggle_llm_mode(self, use_llm: bool):
        """LLMモードの切り替え"""
        self.use_llm = use_llm
        mode = "LLMモード" if use_llm else "ルールベースモード"
        self.logger.info(f"メンターエージェントを{mode}に切り替えました")
    
    def get_llm_status(self) -> Dict[str, Any]:
        """LLMの状態を取得"""
        return {
            "llm_available": self.llm_service.is_available(),
            "llm_enabled": self.use_llm,
            "mode": "hybrid" if self.use_llm and self.llm_service.is_available() else "rule-based"
        }
    
    def load_employee(self, employee_id: str) -> Optional[Employee]:
        """社員データを読み込み"""
        employee_path = self.data_dir / "employees" / f"{employee_id}.json"
        if employee_path.exists():
            with open(employee_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Pydanticバージョン互換性
                if hasattr(Employee, 'model_validate'):
                    # Pydantic v2
                    return Employee.model_validate(data)
                else:
                    # Pydantic v1
                    return Employee(**data)
        return None
    
    def save_employee(self, employee: Employee):
        """社員データを保存"""
        employee_path = self.data_dir / "employees" / f"{employee.id}.json"
        with open(employee_path, "w", encoding="utf-8") as f:
            # Pydanticバージョン互換性のためjson.dumpを使用
            if hasattr(employee, 'model_dump'):
                # Pydantic v2
                data = employee.model_dump()
            else:
                # Pydantic v1
                data = employee.dict()
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    # 新しい自律的エージェント機能
    
    async def autonomous_mentee_support(self, employee: Employee) -> Dict[str, Any]:
        """
        🤖 自律的メンティ支援の実行
        LLMを中心とした完全自律的な成長支援プロセス
        """
        if self.autonomous_mode:
            self.logger.info(f"🚀 自律的メンティ支援を開始: {employee.name}")
            return await self.autonomous_agent.autonomous_mentee_support(employee)
        else:
            # 従来の方式にフォールバック
            return self._traditional_support_process(employee)
    
    async def dynamic_knowledge_search(self, employee: Employee, specific_need: str) -> Dict[str, Any]:
        """
        🔍 動的知識検索
        メンティのニーズに応じた自動情報収集
        """
        if not self.auto_search:
            return {"message": "自動検索は無効化されています"}
        
        self.logger.info(f"🔍 {employee.name}さんのために動的知識検索を実行: {specific_need}")
        
        # 社員コンテキストの構築
        employee_context = {
            "name": employee.name,
            "department": employee.department.value,
            "skills": [skill.name for skill in employee.skills],
            "strengths": employee.strengths,
            "improvement_areas": employee.improvement_areas,
            "learning_pace": employee.learning_pace,
            "preferred_learning_style": employee.preferred_learning_style
        }
        
        # コンテキスト考慮型検索の実行
        search_results = await self.knowledge_search.contextual_knowledge_search(
            employee_context, specific_need
        )
        
        return search_results
    
    async def adaptive_growth_planning(self, employee: Employee, timeframe: int = 90) -> Dict[str, Any]:
        """
        📋 適応的成長計画の作成
        LLMによるタスク分解と個別最適化
        """
        self.logger.info(f"📋 {employee.name}さんの適応的成長計画を作成中... (期間: {timeframe}日)")
        
        # 現状分析の実行
        analysis = self.analyze_employee(employee)
        
        # LLM中心の個別最適化戦略の作成
        growth_strategy = await self.task_planner.create_personalized_growth_strategy(
            employee, analysis
        )
        
        # 適応的リソース発見
        learning_goal = f"{employee.name}さんの技能向上"
        learner_profile = {
            "skill_level": "intermediate",  # 動的に決定
            "learning_style": employee.preferred_learning_style,
            "pace": employee.learning_pace
        }
        
        resources = await self.knowledge_search.adaptive_resource_discovery(
            learning_goal, learner_profile
        )
        
        # 統合された成長計画
        integrated_plan = {
            "employee_id": employee.id,
            "timeframe_days": timeframe,
            "analysis": analysis,
            "growth_strategy": growth_strategy,
            "recommended_resources": resources,
            "created_at": datetime.now().isoformat(),
            "autonomous_features": {
                "auto_adaptation": True,
                "dynamic_milestones": True,
                "risk_monitoring": True,
                "progress_tracking": True
            }
        }
        
        return integrated_plan
    
    async def intelligent_feedback_generation(self, employee: Employee, context: Optional[Dict[str, Any]] = None) -> Feedback:
        """
        💬 知的フィードバック生成
        動的情報収集 + LLM分析による高度フィードバック
        """
        self.logger.info(f"💬 {employee.name}さんの知的フィードバックを生成中...")
        
        # フェーズ1: 動的情報収集
        if self.auto_search:
            search_context = f"{employee.name}の成長に関する最新情報"
            knowledge_results = await self.dynamic_knowledge_search(employee, search_context)
        else:
            knowledge_results = {"message": "自動検索無効"}
        
        # フェーズ2: 深層分析
        analysis = self.analyze_employee(employee)
        
        # フェーズ3: LLM統合フィードバック生成
        enhanced_context = {
            "original_context": context or {},
            "knowledge_results": knowledge_results,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        # 既存のフィードバック生成を拡張
        feedback = self.generate_feedback(employee, enhanced_context)
        
        # 知的機能マーク
        feedback.mentor_id = "autonomous_mentor_agent"
        feedback.is_automated = True
        feedback.confidence_level = 0.95 if self.use_llm else 0.75
        
        return feedback
    
    async def proactive_support_detection(self, employee: Employee) -> Dict[str, Any]:
        """
        🎯 予防的サポート検出
        潜在的な問題を予測し、事前にサポートを提供
        """
        self.logger.info(f"🎯 {employee.name}さんの予防的サポートを検出中...")
        
        # 現状分析
        analysis = self.analyze_employee(employee)
        
        # LLMによる潜在的問題の予測
        if self.llm_service.is_available():
            prediction_prompt = f"""
            {employee.name}さんの状況を分析し、今後30日以内に発生する可能性がある課題や問題を予測してください。
            
            現状分析: {safe_json_dumps(analysis, ensure_ascii=False, indent=2)}
            
            以下の観点で予測:
            - 学習ペースの変化
            - モチベーション低下のリスク
            - スキルギャップの拡大
            - 外部要因の影響
            
            予測結果と推奨される予防的アクションをJSON形式で返してください。
            """
            
            try:
                predictions = await self.llm_service.predict_challenges(prediction_prompt)
                if isinstance(predictions, str):
                    predictions = json.loads(predictions)
            except:
                predictions = {"predicted_challenges": ["学習ペースの維持"], "preventive_actions": ["定期的なチェックイン"]}
        else:
            predictions = {"predicted_challenges": ["学習ペースの維持"], "preventive_actions": ["定期的なチェックイン"]}
        
        # 予防的サポートの生成
        support_actions = []
        for challenge in predictions.get("predicted_challenges", []):
            support = self.provide_support(employee, "proactive_prevention")
            support["target_challenge"] = challenge
            support_actions.append(support)
        
        return {
            "employee_id": employee.id,
            "predictions": predictions,
            "proactive_support": support_actions,
            "confidence_score": 0.8,
            "next_check_date": (datetime.now() + timedelta(days=7)).isoformat()
        }
    
    # 制御メソッド
    
    def enable_autonomous_mode(self, enable: bool = True):
        """自律モードの有効/無効"""
        self.autonomous_mode = enable
        mode = "有効" if enable else "無効"
        self.logger.info(f"🤖 自律モードを{mode}にしました")
    
    def enable_auto_search(self, enable: bool = True):
        """自動検索の有効/無効"""
        self.auto_search = enable
        mode = "有効" if enable else "無効"
        self.logger.info(f"🔍 自動検索を{mode}にしました")
    
    def get_autonomous_status(self) -> Dict[str, Any]:
        """自律的エージェントの状態取得"""
        llm_status = self.get_llm_status()
        return {
            "autonomous_mode": self.autonomous_mode,
            "auto_search": self.auto_search,
            "llm_status": llm_status,
            "available_features": [
                "autonomous_mentee_support",
                "dynamic_knowledge_search", 
                "adaptive_growth_planning",
                "intelligent_feedback_generation",
                "proactive_support_detection"
            ],
            "mode_description": self._get_mode_description()
        }
    
    # ヘルパーメソッド
    
    def _traditional_support_process(self, employee: Employee) -> Dict[str, Any]:
        """従来の支援プロセス（フォールバック）"""
        analysis = self.analyze_employee(employee)
        feedback = self.generate_feedback(employee)
        growth_plan = self.create_growth_plan(employee)
        
        return {
            "mode": "traditional",
            "analysis": analysis,
            "feedback": feedback.dict() if hasattr(feedback, 'dict') else feedback.__dict__,
            "growth_plan": growth_plan,
            "autonomous_features": False
        }
    
    def _get_mode_description(self) -> str:
        """動作モードの説明"""
        if self.autonomous_mode and self.use_llm:
            return "完全自律モード: LLM中心の動的分析・計画・実行"
        elif self.autonomous_mode:
            return "自律モード: ルールベース中心の自動化"
        elif self.use_llm:
            return "LLM支援モード: 手動制御 + AI分析"
        else:
            return "基本モード: ルールベースの従来型支援"
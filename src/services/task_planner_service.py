"""
タスク計画サービス
大タスクを小タスクに分解し、個別最適化された実行計画を生成
"""

import json
import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


def safe_json_dumps(obj, **kwargs):
    """datetime対応のJSONシリアライザー"""
    def default_serializer(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")
    
    return json.dumps(obj, default=default_serializer, **kwargs)

from .llm_service import LLMService
from ..models import Employee


@dataclass
class SubTask:
    """サブタスクの定義"""
    id: str
    name: str
    description: str
    priority: str  # critical, high, medium, low
    complexity: str  # simple, moderate, complex
    estimated_duration: int  # 分
    dependencies: List[str]  # 依存するタスクのID
    required_skills: List[str]
    success_criteria: List[str]
    resources_needed: List[str]
    potential_obstacles: List[str]
    mitigation_strategies: List[str]
    created_at: datetime
    due_date: Optional[datetime] = None
    status: str = "pending"  # pending, in_progress, completed, blocked, failed


@dataclass
class LearningMilestone:
    """学習マイルストーンの定義"""
    id: str
    name: str
    description: str
    target_date: datetime
    success_metrics: List[str]
    validation_methods: List[str]
    reward_system: str
    dependencies: List[str]


@dataclass
class AdaptiveStrategy:
    """適応戦略の定義"""
    strategy_type: str  # learning_pace, difficulty, motivation
    trigger_conditions: List[str]
    adaptations: List[str]
    monitoring_metrics: List[str]
    escalation_criteria: List[str]


class TaskPlannerService:
    """
    LLMを活用してタスクの分解と計画を行う
    個人に最適化された学習戦略を生成
    """
    
    def __init__(self):
        self.llm_service = LLMService()
        self.logger = logging.getLogger(__name__)
        self.planning_history: List[Dict[str, Any]] = []
        
    async def create_personalized_growth_strategy(self, employee: Employee, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """個別最適化成長戦略の作成"""
        self.logger.info(f"📋 {employee.name}さんの個別成長戦略を作成中...")
        
        # LLMによる戦略設計プロンプト
        strategy_prompt = self._create_strategy_prompt(employee, analysis)
        
        # 基本戦略の生成
        base_strategy = await self.llm_service.generate_growth_strategy(strategy_prompt)
        
        # タスク分解の実行
        decomposed_tasks = await self._decompose_growth_tasks(employee, base_strategy, analysis)
        
        # マイルストーンの設定
        milestones = await self._generate_adaptive_milestones(employee, decomposed_tasks, analysis)
        
        # 適応戦略の開発
        adaptive_strategies = await self._develop_adaptive_strategies(employee, analysis)
        
        # リスク評価と軽減策
        risk_assessment = await self._assess_and_mitigate_risks(employee, decomposed_tasks, analysis)
        
        # 統合された成長戦略
        integrated_strategy = {
            "employee_id": employee.id,
            "strategy_id": str(uuid.uuid4()),
            "created_at": datetime.now(),
            "base_strategy": base_strategy,
            "decomposed_tasks": [asdict(task) for task in decomposed_tasks],
            "milestones": [asdict(milestone) for milestone in milestones],
            "adaptive_strategies": [asdict(strategy) for strategy in adaptive_strategies],
            "risk_assessment": risk_assessment,
            "estimated_completion": self._calculate_completion_date(decomposed_tasks),
            "success_probability": await self._calculate_success_probability(employee, decomposed_tasks, analysis)
        }
        
        # 計画履歴に記録
        self.planning_history.append(integrated_strategy)
        
        return integrated_strategy
    
    async def _decompose_growth_tasks(self, employee: Employee, base_strategy: Dict[str, Any], analysis: Dict[str, Any]) -> List[SubTask]:
        """成長タスクの詳細分解"""
        self.logger.info("🔄 成長タスクを詳細分解中...")
        
        decomposition_prompt = f"""
        {employee.name}さんの成長戦略を実行可能な小タスクに分解してください。
        
        基本戦略: {safe_json_dumps(base_strategy, ensure_ascii=False, indent=2)}
        分析結果: {safe_json_dumps(analysis, ensure_ascii=False, indent=2)}
        
        社員の特性:
        - 学習ペース: {employee.learning_pace}
        - 強み: {', '.join(employee.strengths)}
        - 改善領域: {', '.join(employee.improvement_areas)}
        - 完了研修: {', '.join(employee.completed_trainings)}
        
        以下の条件で小タスクに分解してください：
        - 各タスクは1-3日で完了可能
        - 具体的で測定可能な成功基準
        - 依存関係を明確化
        - 学習ペースに適した難易度調整
        - 潜在的な障害と対策を含む
        
        JSON配列形式で返してください：
        [
            {{
                "name": "タスク名",
                "description": "詳細説明",
                "priority": "critical/high/medium/low",
                "complexity": "simple/moderate/complex",
                "estimated_duration": 分数,
                "dependencies": ["依存タスク名"],
                "required_skills": ["必要スキル"],
                "success_criteria": ["成功基準"],
                "resources_needed": ["必要リソース"],
                "potential_obstacles": ["潜在的障害"],
                "mitigation_strategies": ["軽減策"]
            }}
        ]
        """
        
        try:
            decomposed_data = await self.llm_service.decompose_tasks(decomposition_prompt)
            
            if isinstance(decomposed_data, str):
                decomposed_data = json.loads(decomposed_data)
            
            subtasks = []
            for i, task_data in enumerate(decomposed_data):
                subtask = SubTask(
                    id=f"task_{employee.id}_{i+1}_{int(datetime.now().timestamp())}",
                    name=task_data.get("name", f"タスク {i+1}"),
                    description=task_data.get("description", ""),
                    priority=task_data.get("priority", "medium"),
                    complexity=task_data.get("complexity", "moderate"),
                    estimated_duration=task_data.get("estimated_duration", 60),
                    dependencies=task_data.get("dependencies", []),
                    required_skills=task_data.get("required_skills", []),
                    success_criteria=task_data.get("success_criteria", []),
                    resources_needed=task_data.get("resources_needed", []),
                    potential_obstacles=task_data.get("potential_obstacles", []),
                    mitigation_strategies=task_data.get("mitigation_strategies", []),
                    created_at=datetime.now()
                )
                subtasks.append(subtask)
            
            # タスクスケジューリングの最適化
            optimized_tasks = await self._optimize_task_scheduling(subtasks, employee)
            
            return optimized_tasks
            
        except Exception as e:
            self.logger.error(f"タスク分解エラー: {e}")
            # フォールバック: 基本的なタスク分解
            return self._create_fallback_tasks(employee, analysis)
    
    async def _generate_adaptive_milestones(self, employee: Employee, tasks: List[SubTask], analysis: Dict[str, Any]) -> List[LearningMilestone]:
        """適応的マイルストーンの生成"""
        self.logger.info("🎯 適応的マイルストーンを生成中...")
        
        milestone_prompt = f"""
        {employee.name}さんの学習タスクに基づいて、適応的なマイルストーンを設計してください。
        
        タスク情報: {safe_json_dumps([asdict(task) for task in tasks], ensure_ascii=False, indent=2)}
        学習ペース: {employee.learning_pace}
        
        以下の基準でマイルストーンを設計：
        - 学習ペースに応じた間隔調整
        - 具体的で測定可能な成功指標
        - モチベーション維持のための報酬システム
        - 段階的難易度上昇
        - フィードバックループの組み込み
        
        JSON配列で返してください：
        [
            {{
                "name": "マイルストーン名",
                "description": "詳細説明",
                "target_date": "YYYY-MM-DD",
                "success_metrics": ["成功指標"],
                "validation_methods": ["検証方法"],
                "reward_system": "報酬システム",
                "dependencies": ["依存タスクID"]
            }}
        ]
        """
        
        try:
            milestone_data = await self.llm_service.generate_milestones(milestone_prompt)
            
            if isinstance(milestone_data, str):
                milestone_data = json.loads(milestone_data)
            
            milestones = []
            for i, data in enumerate(milestone_data):
                milestone = LearningMilestone(
                    id=f"milestone_{employee.id}_{i+1}_{int(datetime.now().timestamp())}",
                    name=data.get("name", f"マイルストーン {i+1}"),
                    description=data.get("description", ""),
                    target_date=datetime.strptime(data.get("target_date", (datetime.now() + timedelta(weeks=i+1)).strftime("%Y-%m-%d")), "%Y-%m-%d"),
                    success_metrics=data.get("success_metrics", []),
                    validation_methods=data.get("validation_methods", []),
                    reward_system=data.get("reward_system", "基本的な達成認識"),
                    dependencies=data.get("dependencies", [])
                )
                milestones.append(milestone)
            
            return milestones
            
        except Exception as e:
            self.logger.error(f"マイルストーン生成エラー: {e}")
            return self._create_fallback_milestones(employee, tasks)
    
    async def _develop_adaptive_strategies(self, employee: Employee, analysis: Dict[str, Any]) -> List[AdaptiveStrategy]:
        """適応戦略の開発"""
        self.logger.info("🎛️ 適応戦略を開発中...")
        
        strategy_prompt = f"""
        {employee.name}さんの特性に基づいて、学習プロセス中の適応戦略を設計してください。
        
        社員特性:
        - 学習ペース: {employee.learning_pace}
        - 強み: {', '.join(employee.strengths)}
        - 改善領域: {', '.join(employee.improvement_areas)}
        
        分析結果: {safe_json_dumps(analysis, ensure_ascii=False, indent=2)}
        
        以下の戦略タイプを設計：
        1. learning_pace: 学習ペース調整戦略
        2. difficulty: 難易度適応戦略
        3. motivation: モチベーション維持戦略
        4. engagement: エンゲージメント向上戦略
        5. support: サポート強化戦略
        
        各戦略について以下を定義：
        - トリガー条件（どんな状況で発動するか）
        - 具体的な適応内容
        - 監視すべき指標
        - エスカレーション基準
        
        JSON配列で返してください：
        [
            {{
                "strategy_type": "戦略タイプ",
                "trigger_conditions": ["トリガー条件"],
                "adaptations": ["適応内容"],
                "monitoring_metrics": ["監視指標"],
                "escalation_criteria": ["エスカレーション基準"]
            }}
        ]
        """
        
        try:
            strategy_data = await self.llm_service.develop_adaptive_strategies(strategy_prompt)
            
            if isinstance(strategy_data, str):
                strategy_data = json.loads(strategy_data)
            
            strategies = []
            for data in strategy_data:
                strategy = AdaptiveStrategy(
                    strategy_type=data.get("strategy_type", "general"),
                    trigger_conditions=data.get("trigger_conditions", []),
                    adaptations=data.get("adaptations", []),
                    monitoring_metrics=data.get("monitoring_metrics", []),
                    escalation_criteria=data.get("escalation_criteria", [])
                )
                strategies.append(strategy)
            
            return strategies
            
        except Exception as e:
            self.logger.error(f"適応戦略開発エラー: {e}")
            return self._create_fallback_adaptive_strategies(employee)
    
    async def _assess_and_mitigate_risks(self, employee: Employee, tasks: List[SubTask], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """リスク評価と軽減策の策定"""
        self.logger.info("⚠️ リスク評価と軽減策を策定中...")
        
        risk_prompt = f"""
        {employee.name}さんの成長計画におけるリスクを評価し、軽減策を策定してください。
        
        計画されたタスク: {safe_json_dumps([asdict(task) for task in tasks], ensure_ascii=False, indent=2)}
        分析結果: {safe_json_dumps(analysis, ensure_ascii=False, indent=2)}
        
        以下の観点からリスク評価：
        1. 学習ペースとタスク量のミスマッチ
        2. スキルギャップによる実行困難
        3. モチベーション低下の可能性
        4. 時間管理の課題
        5. 外部要因（業務負荷等）の影響
        6. リソース不足のリスク
        
        以下の形式で返してください：
        {{
            "identified_risks": [
                {{
                    "risk_type": "リスクタイプ",
                    "description": "リスク説明",
                    "probability": "発生確率(high/medium/low)",
                    "impact": "影響度(high/medium/low)",
                    "risk_score": "リスクスコア(1-10)"
                }}
            ],
            "mitigation_strategies": [
                {{
                    "risk_type": "対象リスクタイプ",
                    "strategy": "軽減戦略",
                    "preventive_actions": ["予防アクション"],
                    "contingency_plans": ["緊急時計画"]
                }}
            ],
            "monitoring_plan": {{
                "early_warning_indicators": ["早期警告指標"],
                "monitoring_frequency": "監視頻度",
                "escalation_procedures": ["エスカレーション手順"]
            }},
            "overall_risk_level": "全体リスクレベル(low/medium/high)"
        }}
        """
        
        try:
            risk_assessment = await self.llm_service.assess_risks(risk_prompt)
            
            if isinstance(risk_assessment, str):
                risk_assessment = json.loads(risk_assessment)
            
            return risk_assessment
            
        except Exception as e:
            self.logger.error(f"リスク評価エラー: {e}")
            return self._create_fallback_risk_assessment()
    
    async def _optimize_task_scheduling(self, tasks: List[SubTask], employee: Employee) -> List[SubTask]:
        """タスクスケジューリングの最適化"""
        self.logger.info("⏰ タスクスケジューリングを最適化中...")
        
        # 学習ペースに基づく時間調整
        pace_multiplier = 1.0 / employee.learning_pace if employee.learning_pace > 0 else 1.0
        
        optimized_tasks = []
        current_date = datetime.now()
        
        # 依存関係を考慮したスケジューリング
        task_dict = {task.name: task for task in tasks}
        scheduled_tasks = set()
        
        def can_schedule(task: SubTask) -> bool:
            return all(dep in scheduled_tasks for dep in task.dependencies)
        
        while len(scheduled_tasks) < len(tasks):
            schedulable_tasks = [task for task in tasks 
                               if task.name not in scheduled_tasks and can_schedule(task)]
            
            if not schedulable_tasks:
                # 循環依存の解決
                remaining_tasks = [task for task in tasks if task.name not in scheduled_tasks]
                if remaining_tasks:
                    schedulable_tasks = [remaining_tasks[0]]  # 最初のタスクを強制スケジュール
            
            for task in schedulable_tasks:
                # 時間調整
                adjusted_duration = int(task.estimated_duration * pace_multiplier)
                task.estimated_duration = adjusted_duration
                
                # 期限設定
                task.due_date = current_date + timedelta(minutes=adjusted_duration)
                current_date = task.due_date
                
                optimized_tasks.append(task)
                scheduled_tasks.add(task.name)
                
                break  # 一つずつ処理
        
        return optimized_tasks
    
    def _calculate_completion_date(self, tasks: List[SubTask]) -> datetime:
        """完了予定日の計算"""
        if not tasks:
            return datetime.now() + timedelta(days=30)
        
        latest_due_date = max(task.due_date for task in tasks if task.due_date)
        return latest_due_date if latest_due_date else datetime.now() + timedelta(days=30)
    
    async def _calculate_success_probability(self, employee: Employee, tasks: List[SubTask], analysis: Dict[str, Any]) -> float:
        """成功確率の計算"""
        try:
            # 基本確率（学習ペースベース）
            base_probability = min(0.9, employee.learning_pace * 0.7)
            
            # タスク複雑度による調整
            complexity_penalty = 0
            for task in tasks:
                if task.complexity == "complex":
                    complexity_penalty += 0.1
                elif task.complexity == "moderate":
                    complexity_penalty += 0.05
            
            # リスク要因による調整
            risk_factors = analysis.get("risk_factors", [])
            risk_penalty = len(risk_factors) * 0.05
            
            # 最終確率計算
            final_probability = max(0.1, base_probability - complexity_penalty - risk_penalty)
            
            return round(final_probability, 2)
            
        except Exception:
            return 0.7  # デフォルト値
    
    def _create_strategy_prompt(self, employee: Employee, analysis: Dict[str, Any]) -> str:
        """戦略生成プロンプトの作成"""
        return f"""
        {employee.name}さんの個別最適化成長戦略を設計してください。
        
        社員基本情報:
        - 名前: {employee.name}
        - 部署: {employee.department.value}
        - 学習ペース: {employee.learning_pace}
        - 強み: {', '.join(employee.strengths)}
        - 改善領域: {', '.join(employee.improvement_areas)}
        - 完了研修: {', '.join(employee.completed_trainings)}
        - 現在の目標: {', '.join(employee.current_objectives)}
        
        分析結果: {safe_json_dumps(analysis, ensure_ascii=False, indent=2)}
        
        以下の要素を含む包括的戦略を設計：
        1. 個別化学習アプローチ
        2. スキル開発プライオリティ
        3. 段階的成長ロードマップ
        4. モチベーション維持戦略
        5. 進捗測定方法
        6. サポート体制
        
        JSON形式で返してください：
        {{
            "strategic_approach": "戦略的アプローチ",
            "learning_methodology": "学習方法論",
            "skill_priorities": ["スキル優先順位"],
            "growth_phases": [
                {{
                    "phase": "フェーズ名",
                    "duration": "期間",
                    "objectives": ["目標"],
                    "key_activities": ["主要活動"]
                }}
            ],
            "motivation_strategy": "モチベーション戦略",
            "progress_metrics": ["進捗指標"],
            "support_requirements": ["サポート要件"]
        }}
        """
    
    # フォールバックメソッド
    
    def _create_fallback_tasks(self, employee: Employee, analysis: Dict[str, Any]) -> List[SubTask]:
        """フォールバック用の基本タスク作成"""
        basic_tasks = []
        for i, area in enumerate(employee.improvement_areas[:3]):
            task = SubTask(
                id=f"fallback_task_{employee.id}_{i+1}",
                name=f"{area}の改善",
                description=f"{area}に関するスキル向上タスク",
                priority="medium",
                complexity="moderate",
                estimated_duration=120,
                dependencies=[],
                required_skills=[area],
                success_criteria=[f"{area}の基本的な改善"],
                resources_needed=["学習教材", "練習機会"],
                potential_obstacles=["時間不足", "理解困難"],
                mitigation_strategies=["段階的学習", "メンター支援"],
                created_at=datetime.now(),
                due_date=datetime.now() + timedelta(days=7*(i+1))
            )
            basic_tasks.append(task)
        return basic_tasks
    
    def _create_fallback_milestones(self, employee: Employee, tasks: List[SubTask]) -> List[LearningMilestone]:
        """フォールバック用のマイルストーン作成"""
        return [
            LearningMilestone(
                id=f"fallback_milestone_{employee.id}_1",
                name="初期スキル習得",
                description="基本的なスキルの習得",
                target_date=datetime.now() + timedelta(weeks=2),
                success_metrics=["基本課題の完了"],
                validation_methods=["実践テスト"],
                reward_system="達成認識",
                dependencies=[]
            )
        ]
    
    def _create_fallback_adaptive_strategies(self, employee: Employee) -> List[AdaptiveStrategy]:
        """フォールバック用の適応戦略作成"""
        return [
            AdaptiveStrategy(
                strategy_type="learning_pace",
                trigger_conditions=["進捗遅延"],
                adaptations=["タスク分割", "追加サポート"],
                monitoring_metrics=["完了率", "理解度"],
                escalation_criteria=["3日連続遅延"]
            )
        ]
    
    def _create_fallback_risk_assessment(self) -> Dict[str, Any]:
        """フォールバック用のリスク評価作成"""
        return {
            "identified_risks": [
                {
                    "risk_type": "time_management",
                    "description": "時間管理の課題",
                    "probability": "medium",
                    "impact": "medium",
                    "risk_score": "5"
                }
            ],
            "mitigation_strategies": [
                {
                    "risk_type": "time_management",
                    "strategy": "タスク優先順位付け",
                    "preventive_actions": ["スケジュール管理"],
                    "contingency_plans": ["追加サポート提供"]
                }
            ],
            "monitoring_plan": {
                "early_warning_indicators": ["進捗遅延"],
                "monitoring_frequency": "週次",
                "escalation_procedures": ["メンター介入"]
            },
            "overall_risk_level": "medium"
        }
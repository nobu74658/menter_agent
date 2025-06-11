"""
自律的AIエージェントサービス
LLMを中心とした自律的な問題解決とタスク分解を行う
"""

import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


def safe_json_dumps(obj, **kwargs):
    """datetime対応のJSONシリアライザー"""
    def default_serializer(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")
    
    return json.dumps(obj, default=default_serializer, **kwargs)

from .llm_service import LLMService
from .knowledge_search_service import KnowledgeSearchService
from .task_planner_service import TaskPlannerService
from ..models import Employee, Feedback


@dataclass
class Task:
    """実行タスクの定義"""
    id: str
    name: str
    description: str
    priority: str  # high, medium, low
    status: str    # pending, in_progress, completed, failed
    dependencies: List[str]
    estimated_duration: int  # minutes
    required_tools: List[str]
    context: Dict[str, Any]
    created_at: datetime
    due_date: Optional[datetime] = None


@dataclass 
class AgentPlan:
    """エージェントの実行計画"""
    goal: str
    strategy: str
    tasks: List[Task]
    success_criteria: List[str]
    risk_factors: List[str]
    estimated_completion: datetime


class AutonomousAgentService:
    """
    自律的AIエージェントのメインオーケストレーター
    LLMを中心として、メンティの成長支援という大タスクを
    小タスクに分解して自律的に実行する
    """
    
    def __init__(self):
        self.llm_service = LLMService()
        self.knowledge_search = KnowledgeSearchService()
        self.task_planner = TaskPlannerService()
        self.logger = logging.getLogger(__name__)
        
        # エージェントの実行履歴とコンテキスト
        self.execution_history: List[Dict[str, Any]] = []
        self.current_context: Dict[str, Any] = {}
        self.active_plans: List[AgentPlan] = []
        
    async def autonomous_mentee_support(self, employee: Employee) -> Dict[str, Any]:
        """
        メンティ成長支援の自律的実行
        大タスクを小タスクに分解して自動実行
        """
        self.logger.info(f"🤖 自律的メンティ支援を開始: {employee.name}")
        
        # Phase 1: 深層理解タスク
        understanding_result = await self._execute_deep_understanding(employee)
        
        # Phase 2: 動的情報収集タスク  
        knowledge_result = await self._execute_knowledge_gathering(employee, understanding_result)
        
        # Phase 3: 診断・分析タスク
        analysis_result = await self._execute_diagnostic_analysis(employee, understanding_result, knowledge_result)
        
        # Phase 4: 計画立案タスク
        plan_result = await self._execute_strategic_planning(employee, analysis_result)
        
        # Phase 5: 実行支援タスク
        execution_result = await self._execute_support_actions(employee, plan_result)
        
        # Phase 6: 継続改善タスク
        improvement_result = await self._execute_continuous_improvement(employee, execution_result)
        
        # 総合結果の編集
        final_result = await self._synthesize_results(employee, {
            "understanding": understanding_result,
            "knowledge": knowledge_result, 
            "analysis": analysis_result,
            "planning": plan_result,
            "execution": execution_result,
            "improvement": improvement_result
        })
        
        self.logger.info(f"✅ 自律的メンティ支援完了: {employee.name}")
        return final_result
    
    async def _execute_deep_understanding(self, employee: Employee) -> Dict[str, Any]:
        """Phase 1: 深層理解タスクの実行"""
        self.logger.info("🧠 深層理解タスクを実行中...")
        
        # LLMによる深層分析プロンプトの生成
        analysis_prompt = self._create_deep_analysis_prompt(employee)
        
        # LLMによる多角的分析
        understanding_result = await self.llm_service.advanced_analysis(
            prompt=analysis_prompt,
            analysis_type="deep_understanding",
            context={"employee": employee}
        )
        
        # 追加情報が必要な場合の動的質問生成
        if understanding_result.get("needs_more_info"):
            follow_up_questions = await self._generate_follow_up_questions(employee, understanding_result)
            understanding_result["follow_up_questions"] = follow_up_questions
        
        return understanding_result
    
    async def _execute_knowledge_gathering(self, employee: Employee, understanding: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: 動的情報収集タスクの実行"""
        self.logger.info("🔍 動的情報収集タスクを実行中...")
        
        # 理解結果に基づく検索クエリの自動生成
        search_queries = await self._generate_search_queries(employee, understanding)
        
        knowledge_results = {}
        
        for query_type, queries in search_queries.items():
            query_results = []
            for query in queries:
                if query_type == "web_search":
                    result = await self.knowledge_search.web_search(query)
                elif query_type == "technical_search":
                    result = await self.knowledge_search.technical_knowledge_search(query)
                elif query_type == "industry_search":
                    result = await self.knowledge_search.industry_trend_search(query)
                
                query_results.append(result)
            
            knowledge_results[query_type] = query_results
        
        # LLMによる情報の統合と洞察抽出
        integrated_knowledge = await self.llm_service.integrate_knowledge(
            knowledge_results, employee, understanding
        )
        
        return integrated_knowledge
    
    async def _execute_diagnostic_analysis(self, employee: Employee, understanding: Dict[str, Any], knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: 診断・分析タスクの実行"""
        self.logger.info("🔬 診断・分析タスクを実行中...")
        
        # LLMによる包括的診断分析
        diagnostic_prompt = self._create_diagnostic_prompt(employee, understanding, knowledge)
        
        analysis_result = await self.llm_service.diagnostic_analysis(
            prompt=diagnostic_prompt,
            employee=employee,
            context={
                "understanding": understanding,
                "knowledge": knowledge
            }
        )
        
        # 特定されたギャップや課題の詳細分析
        if analysis_result.get("identified_gaps"):
            detailed_analysis = await self._analyze_specific_gaps(
                employee, analysis_result["identified_gaps"], knowledge
            )
            analysis_result["detailed_gap_analysis"] = detailed_analysis
        
        return analysis_result
    
    async def _execute_strategic_planning(self, employee: Employee, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 4: 戦略的計画立案タスクの実行"""  
        self.logger.info("📋 戦略的計画立案タスクを実行中...")
        
        # LLMによる個別最適化戦略の生成
        planning_result = await self.task_planner.create_personalized_growth_strategy(
            employee, analysis
        )
        
        # 動的マイルストーンとKPIの設定
        milestones = await self._generate_dynamic_milestones(employee, planning_result)
        planning_result["dynamic_milestones"] = milestones
        
        # リスク軽減戦略の策定
        risk_mitigation = await self._develop_risk_mitigation_strategies(
            employee, analysis, planning_result
        )
        planning_result["risk_mitigation"] = risk_mitigation
        
        return planning_result
    
    async def _execute_support_actions(self, employee: Employee, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 5: 実行支援タスクの実行"""
        self.logger.info("🚀 実行支援タスクを実行中...")
        
        # 日次・週次アクションプランの生成
        action_plans = await self._generate_action_plans(employee, plan)
        
        # パーソナライズされたガイダンスの作成
        guidance = await self._create_personalized_guidance(employee, plan)
        
        # 進捗トラッキングシステムの設定
        tracking_system = await self._setup_progress_tracking(employee, plan)
        
        # 適応的介入ポイントの特定
        intervention_points = await self._identify_intervention_points(employee, plan)
        
        return {
            "action_plans": action_plans,
            "guidance": guidance,
            "tracking_system": tracking_system,
            "intervention_points": intervention_points
        }
    
    async def _execute_continuous_improvement(self, employee: Employee, execution: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 6: 継続改善タスクの実行"""
        self.logger.info("🔄 継続改善タスクを実行中...")
        
        # 成果測定システムの構築
        measurement_system = await self._build_measurement_system(employee, execution)
        
        # 学習ループの設計
        learning_loop = await self._design_learning_loop(employee, execution)
        
        # 適応戦略の策定
        adaptation_strategy = await self._develop_adaptation_strategy(employee, execution)
        
        return {
            "measurement_system": measurement_system,
            "learning_loop": learning_loop,
            "adaptation_strategy": adaptation_strategy
        }
    
    async def _synthesize_results(self, employee: Employee, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """全ての結果を統合して最終レポートを生成"""
        self.logger.info("📊 結果統合中...")
        
        synthesis_prompt = f"""
        以下は{employee.name}さんに対する包括的な自律的メンティ支援の結果です。
        
        深層理解: {safe_json_dumps(all_results['understanding'], ensure_ascii=False, indent=2)}
        知識収集: {safe_json_dumps(all_results['knowledge'], ensure_ascii=False, indent=2)}
        診断分析: {safe_json_dumps(all_results['analysis'], ensure_ascii=False, indent=2)}
        戦略計画: {safe_json_dumps(all_results['planning'], ensure_ascii=False, indent=2)}
        実行支援: {safe_json_dumps(all_results['execution'], ensure_ascii=False, indent=2)}
        継続改善: {safe_json_dumps(all_results['improvement'], ensure_ascii=False, indent=2)}
        
        これらの結果を統合して、以下の形式で最終的な支援計画を作成してください：
        
        {{
            "executive_summary": "エグゼクティブサマリー",
            "key_insights": ["主要な洞察のリスト"],
            "personalized_roadmap": "個別化されたロードマップ",
            "immediate_actions": ["即座に実行すべきアクション"],
            "success_predictors": ["成功予測要因"],
            "potential_obstacles": ["潜在的な障害"],
            "recommended_resources": ["推奨リソース"],
            "follow_up_schedule": "フォローアップスケジュール"
        }}
        """
        
        final_synthesis = await self.llm_service.synthesize_comprehensive_plan(synthesis_prompt)
        
        # 実行履歴に記録
        self.execution_history.append({
            "employee_id": employee.id,
            "timestamp": datetime.now(),
            "all_results": all_results,
            "final_synthesis": final_synthesis
        })
        
        return final_synthesis
    
    def _create_deep_analysis_prompt(self, employee: Employee) -> str:
        """深層理解のためのプロンプト生成"""
        return f"""あなたは経験豊富なメンタリングエキスパートです。{employee.name}さんの深層理解を行ってください。
        
        基本情報:
        - 名前: {employee.name}
        - 部署: {employee.department.value}
        - 入社日: {employee.hire_date}
        - 学習ペース: {employee.learning_pace}
        - 強み: {', '.join(employee.strengths)}
        - 改善領域: {', '.join(employee.improvement_areas)}
        
        以下の観点から深層分析を行い、JSON形式で返してください：
        
        {{
            "personality_insights": "性格・特性の洞察",
            "learning_style_analysis": "学習スタイルの詳細分析", 
            "motivation_drivers": "主な動機要因",
            "potential_barriers": "成長の潜在的障壁",
            "hidden_strengths": "隠れた強み",
            "optimal_communication_style": "最適なコミュニケーションスタイル",
            "risk_factors": "リスク要因",
            "growth_opportunities": "成長機会",
            "needs_more_info": "追加情報が必要か (true/false)"
        }}"""
    
    def _create_diagnostic_prompt(self, employee: Employee, understanding: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """診断分析のためのプロンプト生成"""
        return f"""{employee.name}さんの包括的診断分析を実施してください。
        
        深層理解結果: {safe_json_dumps(understanding, ensure_ascii=False, indent=2)}
        収集知識: {safe_json_dumps(knowledge, ensure_ascii=False, indent=2)}
        
        以下の観点から診断し、JSON形式で返してください：
        
        {{
            "current_state_assessment": "現状評価",
            "gap_analysis": "ギャップ分析",
            "root_cause_analysis": "根本原因分析",
            "readiness_assessment": "学習準備度評価", 
            "priority_areas": "優先改善領域",
            "success_probability": "成功確率評価",
            "recommended_approach": "推奨アプローチ",
            "timeline_estimation": "タイムライン見積もり",
            "identified_gaps": ["特定されたギャップのリスト"]
        }}"""

    # 追加のヘルパーメソッド
    
    async def _generate_follow_up_questions(self, employee: Employee, understanding: Dict[str, Any]) -> List[str]:
        """追加情報収集のための質問生成"""
        if not self.llm_service.is_available():
            return ["学習に関してどんな困難を感じていますか？"]
        
        question_prompt = f"""
        {employee.name}さんについてより深く理解するために、追加で聞くべき質問を3-5個生成してください。
        
        現在の理解: {safe_json_dumps(understanding, ensure_ascii=False, indent=2)}
        
        質問は以下の観点を含む：
        - 学習動機と目標
        - 過去の経験と成功パターン
        - 現在の課題と懸念事項
        - 優先事項とライフスタイル
        
        JSON配列で返してください: ["質問1", "質問2", ...]
        """
        
        try:
            questions = await self.llm_service.generate_questions(question_prompt)
            return json.loads(questions) if isinstance(questions, str) else questions
        except:
            return ["学習における最大の課題は何ですか？", "どのような学習方法が最も効果的でしたか？"]
    
    async def _generate_search_queries(self, employee: Employee, understanding: Dict[str, Any]) -> Dict[str, List[str]]:
        """検索クエリの自動生成"""
        if not self.llm_service.is_available():
            return self._fallback_search_queries(employee)
        
        query_prompt = f"""
        {employee.name}さんの成長支援のために必要な情報を収集する検索クエリを生成してください。
        
        社員情報: 部署={employee.department.value}, 強み={employee.strengths}, 改善領域={employee.improvement_areas}
        理解度分析: {safe_json_dumps(understanding, ensure_ascii=False, indent=2)}
        
        以下のカテゴリでクエリを生成：
        - web_search: 一般的な情報収集
        - technical_search: 技術・専門情報
        - industry_search: 業界・トレンド情報
        
        JSON形式で返してください：
        {{
            "web_search": ["クエリ1", "クエリ2"],
            "technical_search": ["クエリ1", "クエリ2"],
            "industry_search": ["クエリ1", "クエリ2"]
        }}
        """
        
        try:
            queries = await self.llm_service.generate_search_queries(query_prompt)
            return json.loads(queries) if isinstance(queries, str) else queries
        except:
            return self._fallback_search_queries(employee)
    
    async def _analyze_specific_gaps(self, employee: Employee, gaps: List[str], knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """特定ギャップの詳細分析"""
        gap_analysis = {}
        
        for gap in gaps:
            analysis_prompt = f"""
            {employee.name}さんの「{gap}」に関するギャップを詳細分析してください。
            
            収集された知識: {safe_json_dumps(knowledge, ensure_ascii=False, indent=2)}
            
            以下の観点で分析：
            - ギャップの具体的内容
            - 原因分析
            - 影響度評価
            - 改善の緊急度
            - 推奨学習アプローチ
            
            JSON形式で返してください。
            """
            
            if self.llm_service.is_available():
                try:
                    analysis = await self.llm_service.analyze_gap(analysis_prompt)
                    gap_analysis[gap] = json.loads(analysis) if isinstance(analysis, str) else analysis
                except:
                    gap_analysis[gap] = {"summary": f"{gap}の改善が必要", "priority": "medium"}
            else:
                gap_analysis[gap] = {"summary": f"{gap}の改善が必要", "priority": "medium"}
        
        return gap_analysis
    
    async def _generate_dynamic_milestones(self, employee: Employee, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """動的マイルストーンの生成"""
        if not self.llm_service.is_available():
            return self._fallback_dynamic_milestones()
        
        milestone_prompt = f"""
        {employee.name}さんの成長計画に基づいて、適応的なマイルストーンを設計してください。
        
        計画: {safe_json_dumps(plan, ensure_ascii=False, indent=2)}
        学習ペース: {employee.learning_pace}
        
        マイルストーンの要件:
        - 学習ペースに応じた間隔調整
        - 測定可能な成功指標
        - モチベーション維持要素
        - 段階的難易度上昇
        
        JSON配列で返してください。
        """
        
        try:
            milestones = await self.llm_service.generate_dynamic_milestones(milestone_prompt)
            return json.loads(milestones) if isinstance(milestones, str) else milestones
        except:
            return self._fallback_dynamic_milestones()
    
    async def _develop_risk_mitigation_strategies(self, employee: Employee, analysis: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
        """リスク軽減戦略の策定"""
        if not self.llm_service.is_available():
            return {"strategies": ["基本的なリスク管理"], "monitoring": "週次確認"}
        
        risk_prompt = f"""
        {employee.name}さんの成長計画におけるリスク軽減戦略を策定してください。
        
        分析結果: {safe_json_dumps(analysis, ensure_ascii=False, indent=2)}
        計画: {safe_json_dumps(plan, ensure_ascii=False, indent=2)}
        
        以下を含む軽減戦略:
        - 予防策
        - 早期発見メカニズム
        - 対処プロトコル
        - エスカレーション基準
        
        JSON形式で返してください。
        """
        
        try:
            strategies = await self.llm_service.develop_risk_mitigation(risk_prompt)
            return json.loads(strategies) if isinstance(strategies, str) else strategies
        except:
            return {"strategies": ["基本的なリスク管理"], "monitoring": "週次確認"}
    
    async def _generate_action_plans(self, employee: Employee, plan: Dict[str, Any]) -> Dict[str, Any]:
        """アクションプランの生成"""
        if not self.llm_service.is_available():
            return self._fallback_action_plans()
        
        action_prompt = f"""
        {employee.name}さんの成長計画を日次・週次の具体的アクションに変換してください。
        
        計画: {safe_json_dumps(plan, ensure_ascii=False, indent=2)}
        学習ペース: {employee.learning_pace}
        
        以下を生成:
        - 日次アクション（1-3個）
        - 週次マイルストーン
        - 月次レビューポイント
        
        JSON形式で返してください。
        """
        
        try:
            actions = await self.llm_service.generate_action_plans(action_prompt)
            return json.loads(actions) if isinstance(actions, str) else actions
        except:
            return self._fallback_action_plans()
    
    async def _create_personalized_guidance(self, employee: Employee, plan: Dict[str, Any]) -> Dict[str, Any]:
        """パーソナライズドガイダンスの作成"""
        if not self.llm_service.is_available():
            return {"guidance": "段階的に学習を進めてください", "style": "supportive"}
        
        guidance_prompt = f"""
        {employee.name}さん向けのパーソナライズされたガイダンスを作成してください。
        
        個人特性:
        - 学習ペース: {employee.learning_pace}
        - 強み: {employee.strengths}
        - 学習スタイル: {employee.preferred_learning_style}
        
        計画: {safe_json_dumps(plan, ensure_ascii=False, indent=2)}
        
        以下を含むガイダンス:
        - 個人に最適化されたアドバイス
        - モチベーション維持のメッセージ
        - 具体的な行動指針
        - 困難時のサポート情報
        
        JSON形式で返してください。
        """
        
        try:
            guidance = await self.llm_service.create_personalized_guidance(guidance_prompt)
            return json.loads(guidance) if isinstance(guidance, str) else guidance
        except:
            return {"guidance": "段階的に学習を進めてください", "style": "supportive"}
    
    async def _setup_progress_tracking(self, employee: Employee, plan: Dict[str, Any]) -> Dict[str, Any]:
        """進捗トラッキングシステムの設定"""
        return {
            "tracking_metrics": ["完了率", "理解度", "スキル進捗"],
            "update_frequency": "日次",
            "reporting_schedule": "週次",
            "dashboard_elements": ["進捗グラフ", "マイルストーン状況", "次のアクション"]
        }
    
    async def _identify_intervention_points(self, employee: Employee, plan: Dict[str, Any]) -> List[Dict[str, str]]:
        """介入ポイントの特定"""
        return [
            {
                "trigger": "進捗遅延3日",
                "intervention": "追加サポート提供",
                "escalation": "メンター面談"
            },
            {
                "trigger": "理解度低下",
                "intervention": "学習方法調整",
                "escalation": "カリキュラム見直し"
            }
        ]
    
    async def _build_measurement_system(self, employee: Employee, execution: Dict[str, Any]) -> Dict[str, Any]:
        """成果測定システムの構築"""
        return {
            "kpi_definitions": ["スキル習得度", "実践応用力", "自律学習能力"],
            "measurement_methods": ["実技テスト", "プロジェクト評価", "ピア評価"],
            "baseline_establishment": "現在のスキルレベルを基準点として設定",
            "progress_indicators": ["週次進捗率", "月次成長スコア"],
            "success_thresholds": "80%以上の目標達成率"
        }
    
    async def _design_learning_loop(self, employee: Employee, execution: Dict[str, Any]) -> Dict[str, Any]:
        """学習ループの設計"""
        return {
            "cycle_structure": ["計画→実行→評価→改善"],
            "cycle_duration": "週次サイクル",
            "feedback_mechanisms": ["自己評価", "システム分析", "メンター評価"],
            "adaptation_triggers": ["目標未達", "理解困難", "興味変化"],
            "continuous_improvement": "データドリブンな戦略調整"
        }
    
    async def _develop_adaptation_strategy(self, employee: Employee, execution: Dict[str, Any]) -> Dict[str, Any]:
        """適応戦略の策定"""
        return {
            "adaptation_criteria": ["学習効果", "エンゲージメント", "時間効率"],
            "adjustment_mechanisms": ["難易度調整", "ペース変更", "方法論転換"],
            "personalization_factors": ["学習スタイル", "興味分野", "目標志向"],
            "feedback_integration": "リアルタイムでの戦略調整"
        }
    
    # フォールバックメソッド
    
    def _fallback_search_queries(self, employee: Employee) -> Dict[str, List[str]]:
        """検索クエリのフォールバック"""
        return {
            "web_search": [f"{employee.department.value} skills development", "professional growth tips"],
            "technical_search": [f"{employee.department.value} best practices", "industry standards"],
            "industry_search": [f"{employee.department.value} trends", "future skills requirements"]
        }
    
    def _fallback_dynamic_milestones(self) -> List[Dict[str, Any]]:
        """動的マイルストーンのフォールバック"""
        return [
            {
                "name": "基礎スキル習得",
                "target_date": (datetime.now() + timedelta(weeks=2)).isoformat(),
                "success_metrics": ["基本課題完了"],
                "reward": "進捗認識"
            }
        ]
    
    def _fallback_action_plans(self) -> Dict[str, Any]:
        """アクションプランのフォールバック"""
        return {
            "daily_actions": ["学習教材の研読", "練習問題の実行"],
            "weekly_milestones": ["週次スキルチェック"],
            "monthly_reviews": ["進捗評価と計画調整"]
        }
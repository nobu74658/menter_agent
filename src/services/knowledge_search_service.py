"""
動的知識検索サービス
Web検索、技術情報検索、業界トレンド検索を統合
"""

import json
import asyncio
import logging
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime


def safe_json_dumps(obj, **kwargs):
    """datetime対応のJSONシリアライザー"""
    def default_serializer(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")
    
    return json.dumps(obj, default=default_serializer, **kwargs)

from .llm_service import LLMService


class KnowledgeSearchService:
    """
    メンティのニーズに応じた動的な知識検索を実行
    Web検索、技術情報、業界トレンドを自律的に収集
    """
    
    def __init__(self):
        self.llm_service = LLMService()
        self.logger = logging.getLogger(__name__)
        self.search_history: List[Dict[str, Any]] = []
        
    async def web_search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Web検索の実行（WebSearchツールの活用）"""
        self.logger.info(f"🌐 Web検索実行: {query}")
        
        try:
            # WebSearchツールを使用（実際の実装では適切なAPI呼び出し）
            search_results = await self._execute_web_search(query, max_results)
            
            # LLMによる検索結果の要約と関連性評価
            analyzed_results = await self._analyze_search_results(query, search_results)
            
            # 検索履歴に記録
            self.search_history.append({
                "timestamp": datetime.now(),
                "query": query,
                "type": "web_search",
                "results_count": len(search_results),
                "relevance_score": analyzed_results.get("average_relevance", 0)
            })
            
            return analyzed_results
            
        except Exception as e:
            self.logger.error(f"Web検索エラー: {e}")
            return {"error": str(e), "results": []}
    
    async def technical_knowledge_search(self, query: str, domain: str = "general") -> Dict[str, Any]:
        """技術知識の専門検索"""
        self.logger.info(f"🔧 技術知識検索実行: {query} (ドメイン: {domain})")
        
        # ドメイン特化型クエリの生成
        specialized_queries = await self._generate_technical_queries(query, domain)
        
        all_results = []
        for spec_query in specialized_queries:
            # 技術情報源での検索
            results = await self._search_technical_sources(spec_query, domain)
            all_results.extend(results)
        
        # 重複除去と関連性ランキング
        ranked_results = await self._rank_and_deduplicate(all_results, query)
        
        # LLMによる技術情報の統合と洞察抽出
        technical_insights = await self._extract_technical_insights(ranked_results, query, domain)
        
        return {
            "query": query,
            "domain": domain,
            "results": ranked_results,
            "technical_insights": technical_insights,
            "confidence_score": technical_insights.get("confidence", 0.7)
        }
    
    async def industry_trend_search(self, industry: str, focus_area: str = None) -> Dict[str, Any]:
        """業界トレンド検索"""
        self.logger.info(f"📈 業界トレンド検索実行: {industry} (フォーカス: {focus_area})")
        
        # トレンド検索クエリの生成
        trend_queries = await self._generate_trend_queries(industry, focus_area)
        
        trend_data = {}
        for query_type, queries in trend_queries.items():
            query_results = []
            for query in queries:
                result = await self._search_trend_sources(query, query_type)
                query_results.append(result)
            trend_data[query_type] = query_results
        
        # トレンド分析とパターン抽出
        trend_analysis = await self._analyze_industry_trends(trend_data, industry, focus_area)
        
        return {
            "industry": industry,
            "focus_area": focus_area,
            "trend_data": trend_data,
            "trend_analysis": trend_analysis,
            "last_updated": datetime.now().isoformat()
        }
    
    async def contextual_knowledge_search(self, employee_context: Dict[str, Any], specific_need: str) -> Dict[str, Any]:
        """コンテキスト考慮型知識検索"""
        self.logger.info(f"🎯 コンテキスト型検索実行: {specific_need}")
        
        # 社員のコンテキストに基づくクエリ生成
        contextual_queries = await self._generate_contextual_queries(employee_context, specific_need)
        
        # 複数ソースからの情報収集
        search_tasks = []
        for query_info in contextual_queries:
            if query_info["type"] == "web":
                task = self.web_search(query_info["query"])
            elif query_info["type"] == "technical":
                task = self.technical_knowledge_search(query_info["query"], query_info.get("domain", "general"))
            elif query_info["type"] == "industry":
                task = self.industry_trend_search(query_info.get("industry"), query_info.get("focus"))
            
            search_tasks.append(task)
        
        # 並行検索実行
        search_results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # 結果の統合と関連性評価
        integrated_results = await self._integrate_contextual_results(
            search_results, employee_context, specific_need
        )
        
        return integrated_results
    
    async def adaptive_resource_discovery(self, learning_goal: str, learner_profile: Dict[str, Any]) -> Dict[str, Any]:
        """学習者に適応したリソース発見"""
        self.logger.info(f"📚 適応的リソース発見: {learning_goal}")
        
        # 学習者プロファイルに基づくリソース検索
        resource_queries = await self._generate_resource_queries(learning_goal, learner_profile)
        
        discovered_resources = {}
        for resource_type, queries in resource_queries.items():
            type_results = []
            for query in queries:
                resources = await self._search_learning_resources(query, resource_type, learner_profile)
                type_results.extend(resources)
            
            # リソースの品質評価とランキング
            ranked_resources = await self._evaluate_and_rank_resources(
                type_results, learning_goal, learner_profile
            )
            discovered_resources[resource_type] = ranked_resources
        
        # パーソナライズされた学習パスの提案
        learning_path = await self._suggest_learning_path(discovered_resources, learning_goal, learner_profile)
        
        return {
            "learning_goal": learning_goal,
            "learner_profile": learner_profile,
            "discovered_resources": discovered_resources,
            "suggested_learning_path": learning_path,
            "personalization_score": learning_path.get("personalization_score", 0.7)
        }
    
    # プライベートメソッド
    
    async def _execute_web_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """実際のWeb検索実行（WebSearchツール統合）"""
        # 実際の実装では、利用可能なWebSearchツールを呼び出し
        # ここではモックデータを返す
        mock_results = [
            {
                "title": f"検索結果 {i+1}: {query}",
                "url": f"https://example.com/result-{i+1}",
                "snippet": f"この結果は{query}に関する有用な情報を含んでいます。",
                "relevance_score": 0.8 - (i * 0.1)
            }
            for i in range(min(max_results, 3))
        ]
        return mock_results
    
    async def _analyze_search_results(self, query: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """LLMによる検索結果の分析"""
        analysis_prompt = f"""
        以下の検索結果を分析し、クエリ「{query}」との関連性と有用性を評価してください。
        
        検索結果: {safe_json_dumps(results, ensure_ascii=False, indent=2)}
        
        以下の形式で分析結果を返してください：
        {{
            "summary": "検索結果の要約",
            "key_insights": ["主要な洞察のリスト"],
            "relevance_scores": [各結果の関連性スコア（0-1）],
            "average_relevance": 平均関連性スコア,
            "recommended_actions": ["推奨アクション"],
            "additional_search_suggestions": ["追加検索提案"]
        }}
        """
        
        if self.llm_service.is_available():
            try:
                analysis = await self.llm_service.analyze_content(analysis_prompt)
                return json.loads(analysis) if isinstance(analysis, str) else analysis
            except Exception as e:
                self.logger.warning(f"LLM分析失敗: {e}")
        
        # フォールバック: 簡単な分析
        return {
            "summary": f"「{query}」に関する{len(results)}件の検索結果",
            "key_insights": ["基本的な情報が収集されました"],
            "relevance_scores": [result.get("relevance_score", 0.5) for result in results],
            "average_relevance": sum(result.get("relevance_score", 0.5) for result in results) / len(results) if results else 0,
            "recommended_actions": ["結果を詳しく確認してください"],
            "additional_search_suggestions": []
        }
    
    async def _generate_technical_queries(self, query: str, domain: str) -> List[str]:
        """技術ドメイン特化型クエリの生成"""
        generation_prompt = f"""
        「{query}」について、{domain}ドメインでの技術検索に最適化されたクエリを3-5個生成してください。
        
        要求:
        - 専門用語を適切に使用
        - 検索効率を最大化
        - 具体的で実践的な情報を取得できる形式
        
        JSON配列形式で返してください: ["クエリ1", "クエリ2", ...]
        """
        
        if self.llm_service.is_available():
            try:
                generated = await self.llm_service.generate_queries(generation_prompt)
                return json.loads(generated) if isinstance(generated, str) else generated
            except:
                pass
        
        # フォールバック
        return [
            f"{query} {domain} best practices",
            f"{query} {domain} tutorial guide",
            f"{query} {domain} implementation example"
        ]
    
    async def _search_technical_sources(self, query: str, domain: str) -> List[Dict[str, Any]]:
        """技術情報源での検索"""
        # 実際の実装では技術文書、API docs、GitHub等を検索
        return [
            {
                "source": "技術文書",
                "title": f"{domain}: {query}",
                "content": f"{query}に関する技術的な詳細情報",
                "relevance": 0.85,
                "authority_score": 0.9
            }
        ]
    
    async def _rank_and_deduplicate(self, results: List[Dict[str, Any]], original_query: str) -> List[Dict[str, Any]]:
        """結果のランキングと重複除去"""
        # 簡単な重複除去とスコアベースのソート
        unique_results = []
        seen_titles = set()
        
        for result in results:
            title = result.get("title", "")
            if title not in seen_titles:
                seen_titles.add(title)
                unique_results.append(result)
        
        # 関連性スコアでソート
        return sorted(unique_results, key=lambda x: x.get("relevance", 0), reverse=True)
    
    async def _extract_technical_insights(self, results: List[Dict[str, Any]], query: str, domain: str) -> Dict[str, Any]:
        """技術情報からの洞察抽出"""
        if not results:
            return {"insights": [], "confidence": 0.0}
        
        insights_prompt = f"""
        以下の技術検索結果から、「{query}」（{domain}ドメイン）に関する重要な洞察を抽出してください。
        
        検索結果: {safe_json_dumps(results, ensure_ascii=False, indent=2)}
        
        以下の形式で返してください：
        {{
            "insights": ["洞察1", "洞察2", ...],
            "best_practices": ["ベストプラクティス1", ...],
            "common_pitfalls": ["よくある落とし穴1", ...],
            "recommended_tools": ["推奨ツール1", ...],
            "confidence": 信頼度スコア（0-1）
        }}
        """
        
        if self.llm_service.is_available():
            try:
                insights = await self.llm_service.extract_insights(insights_prompt)
                return json.loads(insights) if isinstance(insights, str) else insights
            except:
                pass
        
        return {
            "insights": [f"{domain}での{query}に関する基本情報が収集されました"],
            "best_practices": [],
            "common_pitfalls": [],
            "recommended_tools": [],
            "confidence": 0.6
        }
    
    async def _generate_trend_queries(self, industry: str, focus_area: str = None) -> Dict[str, List[str]]:
        """業界トレンド検索クエリの生成"""
        base_queries = {
            "market_trends": [f"{industry} market trends 2024", f"{industry} industry outlook"],
            "technology_trends": [f"{industry} technology trends", f"emerging tech {industry}"],
            "skill_demands": [f"{industry} skills demand", f"in-demand skills {industry}"]
        }
        
        if focus_area:
            for category in base_queries:
                base_queries[category].append(f"{focus_area} {industry} trends")
        
        return base_queries
    
    async def _search_trend_sources(self, query: str, query_type: str) -> Dict[str, Any]:
        """トレンドソースでの検索"""
        # 実際の実装では業界レポート、ニュース、調査データを検索
        return {
            "query": query,
            "type": query_type,
            "data": f"{query}に関するトレンドデータ",
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.75
        }
    
    async def _analyze_industry_trends(self, trend_data: Dict[str, Any], industry: str, focus_area: str) -> Dict[str, Any]:
        """業界トレンドの分析"""
        analysis_prompt = f"""
        {industry}業界のトレンドデータを分析してください。
        フォーカスエリア: {focus_area}
        
        データ: {safe_json_dumps(trend_data, ensure_ascii=False, indent=2)}
        
        以下の形式で分析結果を返してください：
        {{
            "key_trends": ["主要トレンド1", "主要トレンド2", ...],
            "emerging_opportunities": ["新興機会1", ...],
            "skill_requirements": ["必要スキル1", ...],
            "future_outlook": "将来展望",
            "implications_for_learning": "学習への示唆"
        }}
        """
        
        if self.llm_service.is_available():
            try:
                analysis = await self.llm_service.analyze_trends(analysis_prompt)
                return json.loads(analysis) if isinstance(analysis, str) else analysis
            except:
                pass
        
        return {
            "key_trends": [f"{industry}業界の基本的なトレンド"],
            "emerging_opportunities": [],
            "skill_requirements": [],
            "future_outlook": "継続的な成長が期待されます",
            "implications_for_learning": "基本スキルの習得が重要です"
        }
    
    # 追加のメソッドは実装を継続...
    
    async def _generate_contextual_queries(self, employee_context: Dict[str, Any], specific_need: str) -> List[Dict[str, str]]:
        """コンテキストベースクエリ生成"""
        return [
            {"type": "web", "query": f"{specific_need} for {employee_context.get('department', 'general')}"},
            {"type": "technical", "query": specific_need, "domain": employee_context.get('department', 'general')}
        ]
    
    async def _integrate_contextual_results(self, results: List[Any], context: Dict[str, Any], need: str) -> Dict[str, Any]:
        """コンテキスト結果の統合"""
        valid_results = [r for r in results if not isinstance(r, Exception)]
        return {
            "integrated_results": valid_results,
            "context_relevance": 0.8,
            "recommendation": f"{need}に関する情報が収集されました"
        }
    
    async def _generate_resource_queries(self, goal: str, profile: Dict[str, Any]) -> Dict[str, List[str]]:
        """リソース検索クエリ生成"""
        return {
            "courses": [f"{goal} online course", f"{goal} training"],
            "books": [f"{goal} book recommendation", f"best books {goal}"],
            "tools": [f"{goal} tools", f"{goal} software"]
        }
    
    async def _search_learning_resources(self, query: str, resource_type: str, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """学習リソース検索"""
        return [
            {
                "title": f"{resource_type}: {query}",
                "type": resource_type,
                "quality_score": 0.8,
                "difficulty_level": profile.get("skill_level", "beginner")
            }
        ]
    
    async def _evaluate_and_rank_resources(self, resources: List[Dict[str, Any]], goal: str, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """リソース評価とランキング"""
        return sorted(resources, key=lambda x: x.get("quality_score", 0), reverse=True)
    
    async def _suggest_learning_path(self, resources: Dict[str, Any], goal: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """学習パス提案"""
        return {
            "path_steps": ["ステップ1: 基礎学習", "ステップ2: 実践演習"],
            "estimated_duration": "30日",
            "personalization_score": 0.85
        }
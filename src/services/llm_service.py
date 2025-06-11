import os
import json
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta


def safe_json_dumps(obj, **kwargs):
    """datetime対応のJSONシリアライザー"""
    def default_serializer(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")
    
    return json.dumps(obj, default=default_serializer, **kwargs)

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from config.config import settings
from ..models import Employee, Feedback, FeedbackType


class LLMService:
    """LLM（OpenAI）サービスクラス"""
    
    def __init__(self):
        self.client = None
        self.logger = logging.getLogger(__name__)
        self._initialize_client()
    
    def _initialize_client(self):
        """OpenAIクライアントの初期化"""
        if not OPENAI_AVAILABLE:
            self.logger.warning("OpenAI library not available. LLM features will be disabled.")
            return
            
        try:
            api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                self.logger.warning("OpenAI API key not found. LLM features will be disabled.")
                return
            
            # OpenAI 1.0+ クライアントの初期化
            try:
                # 環境変数から不要なプロキシ設定を一時的に削除
                proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
                old_proxy_values = {}
                for var in proxy_vars:
                    if var in os.environ:
                        old_proxy_values[var] = os.environ[var]
                        del os.environ[var]
                
                self.client = OpenAI(api_key=api_key)
                
                # プロキシ設定を復元
                for var, value in old_proxy_values.items():
                    os.environ[var] = value
                    
                self.logger.info("OpenAI client initialized successfully")
            except TypeError as te:
                if "proxies" in str(te):
                    # 完全フォールバック: LLMを無効化
                    self.logger.warning("OpenAI client initialization failed due to proxy configuration. Disabling LLM features.")
                    self.client = None
                    return
                else:
                    raise te
            
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def is_available(self) -> bool:
        """LLMサービスが利用可能かチェック"""
        return self.client is not None
    
    def generate_personalized_feedback(
        self, 
        employee: Employee, 
        analysis: Dict[str, Any], 
        feedback_type: FeedbackType
    ) -> Optional[Dict[str, str]]:
        """個別化されたフィードバックを生成"""
        if not self.is_available():
            return None
        
        try:
            prompt = self._create_feedback_prompt(employee, analysis, feedback_type)
            
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # JSONパース試行、失敗時は代替フォーマット
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # JSONでない場合は基本フォーマットを作成
                result = {
                    "summary": f"{employee.name}さんへのAIフィードバック",
                    "detailed": content[:400] if content else "AIによる詳細分析です。",
                    "encouragement": "継続的な努力を続けてください！",
                    "next_steps": "次のステップに向けて準備を進めましょう。"
                }
            
            self.logger.info(f"Generated LLM feedback for employee {employee.id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to generate LLM feedback: {e}")
            return None
    
    def generate_growth_recommendations(
        self, 
        employee: Employee, 
        analysis: Dict[str, Any]
    ) -> Optional[List[str]]:
        """成長のための推奨事項を生成"""
        if not self.is_available():
            return None
        
        try:
            prompt = self._create_recommendations_prompt(employee, analysis)
            
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは経験豊富な人材育成コンサルタントです。新人社員の成長を支援する具体的で実行可能な推奨事項を日本語で提供してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            # 推奨事項をリストに分割
            recommendations = [
                rec.strip().lstrip("・-•").strip() 
                for rec in content.split('\n') 
                if rec.strip() and not rec.strip().startswith('#')
            ]
            
            self.logger.info(f"Generated {len(recommendations)} LLM recommendations for employee {employee.id}")
            return recommendations[:5]  # 最大5つの推奨事項
            
        except Exception as e:
            self.logger.error(f"Failed to generate LLM recommendations: {e}")
            return None
    
    def generate_support_message(
        self, 
        employee: Employee, 
        issue_type: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """サポートメッセージを生成"""
        if not self.is_available():
            return None
        
        try:
            prompt = self._create_support_prompt(employee, issue_type, context)
            
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは親身で経験豊富なメンターです。新人社員の課題に対して、励ましとともに具体的なサポートを日本語で提供してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=400,
                temperature=0.8
            )
            
            content = response.choices[0].message.content.strip()
            self.logger.info(f"Generated LLM support message for employee {employee.id}, issue: {issue_type}")
            return content
            
        except Exception as e:
            self.logger.error(f"Failed to generate LLM support message: {e}")
            return None
    
    def _get_system_prompt(self) -> str:
        """システムプロンプト"""
        return """あなたは新人社員を指導する経験豊富で親身なメンターです。

役割：
- 新人社員の成長を支援し、動機付けを行う
- 建設的で具体的なフィードバックを提供する
- 日本のビジネス文化に適した丁寧で親しみやすい言葉遣いを使用する
- 個人の特性と学習スタイルに配慮したアドバイスを行う

出力形式：
必ずJSON形式で以下の構造で回答してください：
{
  "summary": "フィードバックの要約（50文字以内）",
  "detailed": "詳細なフィードバック（200-400文字）",
  "encouragement": "励ましのメッセージ（100文字以内）",
  "next_steps": "次のステップの提案（150文字以内）"
}"""
    
    def _create_feedback_prompt(
        self, 
        employee: Employee, 
        analysis: Dict[str, Any], 
        feedback_type: FeedbackType
    ) -> str:
        """フィードバック生成用プロンプト"""
        
        feedback_type_descriptions = {
            FeedbackType.POSITIVE: "成果を認識し、更なる成長を促すポジティブなフィードバック",
            FeedbackType.CONSTRUCTIVE: "改善点を建設的に指摘し、具体的な改善方法を提案するフィードバック",
            FeedbackType.DEVELOPMENTAL: "成長のための具体的な開発計画を含む支援的なフィードバック",
            FeedbackType.RECOGNITION: "優れた成果を称賛し、さらなる挑戦を促すフィードバック"
        }
        
        return f"""
社員情報：
- 名前: {employee.name}
- 部署: {employee.department.value}
- 入社からの日数: {(employee.created_at - employee.hire_date).days}日
- 学習ペース: {employee.learning_pace}
- 学習スタイル: {employee.preferred_learning_style}

分析結果：
- 総合評価: {analysis.get('overall_assessment', 'N/A')}
- 成長軌道: {analysis.get('growth_trajectory', 'N/A')}
- 強み: {', '.join(employee.strengths[:3])}
- 改善領域: {', '.join(employee.improvement_areas[:3])}
- リスク要因: {', '.join(analysis.get('risk_factors', []))}

スキル状況：
{self._format_skills(employee.skills)}

フィードバックタイプ: {feedback_type_descriptions.get(feedback_type, feedback_type.value)}

上記の情報に基づいて、{employee.name}さんに対する個別化されたフィードバックを生成してください。
学習ペース（{employee.learning_pace}）を考慮し、適切な難易度とペースでアドバイスを提供してください。
"""
    
    def _create_recommendations_prompt(
        self, 
        employee: Employee, 
        analysis: Dict[str, Any]
    ) -> str:
        """推奨事項生成用プロンプト"""
        return f"""
{employee.name}さんの成長のための具体的な推奨事項を5つ以内で提案してください。

社員情報：
- 学習ペース: {employee.learning_pace}
- 強み: {', '.join(employee.strengths)}
- 改善領域: {', '.join(employee.improvement_areas)}
- 完了した研修: {', '.join(employee.completed_trainings)}
- 現在の目標: {', '.join(employee.current_objectives)}

分析結果：
- 成長ポテンシャル: {analysis.get('growth_potential', 'N/A')}
- リスク要因: {', '.join(analysis.get('risk_factors', []))}

実行可能で具体的な推奨事項を、優先度の高い順に提案してください。
各推奨事項は1行で、40文字以内にまとめてください。
"""
    
    def _create_support_prompt(
        self, 
        employee: Employee, 
        issue_type: str, 
        context: Optional[Dict[str, Any]]
    ) -> str:
        """サポートメッセージ生成用プロンプト"""
        
        issue_descriptions = {
            "skill_gap": "特定のスキルが不足している状況",
            "motivation": "モチベーションが低下している状況", 
            "communication": "コミュニケーションに課題がある状況",
            "workload": "作業負荷が過多な状況",
            "learning_pace": "学習ペースに問題がある状況"
        }
        
        return f"""
{employee.name}さんが以下の課題に直面しています：
課題: {issue_descriptions.get(issue_type, issue_type)}

社員の特性：
- 学習ペース: {employee.learning_pace}
- 強み: {', '.join(employee.strengths[:3])}
- 学習スタイル: {employee.preferred_learning_style}

この課題に対して、{employee.name}さんを励まし、具体的なサポートを提供するメッセージを作成してください。
メッセージは温かく親身でありながら、実用的なアドバイスを含めてください。
200文字以内でまとめてください。
"""
    
    def _format_skills(self, skills: List) -> str:
        """スキル情報をフォーマット"""
        if not skills:
            return "スキル情報なし"
        
        skill_text = ""
        for skill in skills[:5]:  # 最大5つのスキル
            skill_text += f"- {skill.name}: {skill.level.value} (進捗: {skill.progress_rate}%)\n"
        
        return skill_text.strip()
    
    # 自律的エージェント用の高度な機能
    
    async def advanced_analysis(self, prompt: str, analysis_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """高度な分析機能（非同期対応）"""
        if not self.is_available():
            return {"error": "LLM not available", "fallback": True}
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_advanced_system_prompt(analysis_type)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1200,
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                result = {
                    "analysis": content,
                    "confidence": 0.7,
                    "needs_more_info": False
                }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Advanced analysis failed: {e}")
            return {"error": str(e), "fallback": True}
    
    async def generate_growth_strategy(self, prompt: str) -> Dict[str, Any]:
        """成長戦略生成"""
        if not self.is_available():
            return self._fallback_growth_strategy()
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": """あなたは人材開発のエキスパートです。個人の特性と分析結果に基づいて、
                        効果的で実行可能な成長戦略を設計してください。戦略は具体的で測定可能である必要があります。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "strategic_approach": content[:200] + "...",
                    "learning_methodology": "段階的学習アプローチ",
                    "skill_priorities": ["基本スキル習得"],
                    "growth_phases": [{"phase": "基礎", "duration": "30日", "objectives": ["基本習得"]}]
                }
            
        except Exception as e:
            self.logger.error(f"Growth strategy generation failed: {e}")
            return self._fallback_growth_strategy()
    
    async def decompose_tasks(self, prompt: str) -> List[Dict[str, Any]]:
        """タスク分解"""
        if not self.is_available():
            return self._fallback_task_decomposition()
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": """あなたはプロジェクト管理の専門家です。大きなタスクを実行可能な小さなタスクに
                        分解してください。各タスクは具体的で、明確な成功基準と期限を持つ必要があります。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.5
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # 分解失敗時のフォールバック
                return self._fallback_task_decomposition()
            
        except Exception as e:
            self.logger.error(f"Task decomposition failed: {e}")
            return self._fallback_task_decomposition()
    
    async def generate_milestones(self, prompt: str) -> List[Dict[str, Any]]:
        """マイルストーン生成"""
        if not self.is_available():
            return self._fallback_milestones()
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": """あなたは学習設計の専門家です。効果的なマイルストーンを設計し、
                        学習者のモチベーション維持と進捗測定を支援してください。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return self._fallback_milestones()
            
        except Exception as e:
            self.logger.error(f"Milestone generation failed: {e}")
            return self._fallback_milestones()
    
    async def develop_adaptive_strategies(self, prompt: str) -> List[Dict[str, Any]]:
        """適応戦略開発"""
        if not self.is_available():
            return self._fallback_adaptive_strategies()
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": """あなたは適応学習システムの専門家です。学習者の状況変化に応じて
                        自動的に調整される戦略を設計してください。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return self._fallback_adaptive_strategies()
            
        except Exception as e:
            self.logger.error(f"Adaptive strategy development failed: {e}")
            return self._fallback_adaptive_strategies()
    
    async def assess_risks(self, prompt: str) -> Dict[str, Any]:
        """リスク評価"""
        if not self.is_available():
            return self._fallback_risk_assessment()
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": """あなたはリスク管理の専門家です。学習・成長プロセスにおける潜在的なリスクを
                        特定し、効果的な軽減策を提案してください。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1200,
                temperature=0.5
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return self._fallback_risk_assessment()
            
        except Exception as e:
            self.logger.error(f"Risk assessment failed: {e}")
            return self._fallback_risk_assessment()
    
    async def integrate_knowledge(self, knowledge_results: Dict[str, Any], employee, understanding: Dict[str, Any]) -> Dict[str, Any]:
        """知識統合"""
        if not self.is_available():
            return {"integrated_insights": ["基本的な知識が収集されました"], "confidence": 0.5}
        
        integration_prompt = f"""
        以下の知識検索結果を統合し、{employee.name}さんの学習に最も関連する洞察を抽出してください。
        
        検索結果: {safe_json_dumps(knowledge_results, ensure_ascii=False, indent=2)}
        理解度分析: {safe_json_dumps(understanding, ensure_ascii=False, indent=2)}
        
        以下の形式で統合結果を返してください：
        {{
            "integrated_insights": ["統合された洞察"],
            "relevant_resources": ["関連リソース"],
            "actionable_recommendations": ["実行可能な推奨事項"],
            "confidence": 信頼度（0-1）
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは情報統合の専門家です。複数の情報源から価値ある洞察を抽出し、学習者に最適化された形で提示してください。"
                    },
                    {
                        "role": "user",
                        "content": integration_prompt
                    }
                ],
                max_tokens=800,
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "integrated_insights": [content[:200] + "..."],
                    "relevant_resources": [],
                    "actionable_recommendations": [],
                    "confidence": 0.6
                }
            
        except Exception as e:
            self.logger.error(f"Knowledge integration failed: {e}")
            return {"integrated_insights": ["基本的な知識が収集されました"], "confidence": 0.4}
    
    async def diagnostic_analysis(self, prompt: str, employee, context: Dict[str, Any]) -> Dict[str, Any]:
        """診断分析"""
        if not self.is_available():
            return self._fallback_diagnostic_analysis()
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは学習診断の専門家です。個人の学習状況を包括的に分析し、具体的な改善策を提案してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return self._fallback_diagnostic_analysis()
            
        except Exception as e:
            self.logger.error(f"Diagnostic analysis failed: {e}")
            return self._fallback_diagnostic_analysis()
    
    async def synthesize_comprehensive_plan(self, prompt: str) -> Dict[str, Any]:
        """包括的計画の統合"""
        if not self.is_available():
            return self._fallback_comprehensive_plan()
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは戦略統合の専門家です。複数の分析結果を統合し、実行可能で包括的なアクションプランを作成してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "executive_summary": content[:300] + "...",
                    "key_insights": ["包括的な分析が完了しました"],
                    "personalized_roadmap": "個別化されたロードマップが作成されました",
                    "immediate_actions": ["優先アクションを実行してください"]
                }
            
        except Exception as e:
            self.logger.error(f"Comprehensive plan synthesis failed: {e}")
            return self._fallback_comprehensive_plan()
    
    # ヘルパーメソッド
    
    def _get_advanced_system_prompt(self, analysis_type: str) -> str:
        """高度分析用システムプロンプト"""
        prompts = {
            "deep_understanding": """あなたは心理学と学習理論の専門家です。個人の深層的な特性と
            学習パターンを分析し、最適化された成長戦略の基盤となる洞察を提供してください。""",
            
            "diagnostic_analysis": """あなたは診断学習の専門家です。学習者の現状を多角的に分析し、
            成長の阻害要因と促進要因を特定してください。""",
            
            "strategic_planning": """あなたは戦略的人材開発の専門家です。分析結果に基づいて、
            実行可能で効果的な成長戦略を設計してください。"""
        }
        
        return prompts.get(analysis_type, "あなたは人材開発の専門家です。")
    
    # フォールバックメソッド
    
    def _fallback_growth_strategy(self) -> Dict[str, Any]:
        """成長戦略のフォールバック"""
        return {
            "strategic_approach": "段階的スキル習得アプローチ",
            "learning_methodology": "実践的学習と理論の組み合わせ",
            "skill_priorities": ["基本スキル", "応用スキル", "実践スキル"],
            "growth_phases": [
                {
                    "phase": "基礎固め",
                    "duration": "30日",
                    "objectives": ["基本概念の理解"],
                    "key_activities": ["学習教材の研究", "基礎練習"]
                }
            ],
            "motivation_strategy": "小さな成功の積み重ね",
            "progress_metrics": ["完了率", "理解度テスト"],
            "support_requirements": ["定期的なフィードバック", "リソース提供"]
        }
    
    def _fallback_task_decomposition(self) -> List[Dict[str, Any]]:
        """タスク分解のフォールバック"""
        return [
            {
                "name": "基礎学習",
                "description": "基本的な概念と原理の学習",
                "priority": "high",
                "complexity": "simple",
                "estimated_duration": 120,
                "dependencies": [],
                "required_skills": ["読解力"],
                "success_criteria": ["基本概念の理解"],
                "resources_needed": ["学習教材"],
                "potential_obstacles": ["時間不足"],
                "mitigation_strategies": ["スケジュール管理"]
            }
        ]
    
    def _fallback_milestones(self) -> List[Dict[str, Any]]:
        """マイルストーンのフォールバック"""
        return [
            {
                "name": "初期目標達成",
                "description": "最初のマイルストーンの達成",
                "target_date": (datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d"),
                "success_metrics": ["基本課題の完了"],
                "validation_methods": ["実践テスト"],
                "reward_system": "達成証明書",
                "dependencies": []
            }
        ]
    
    def _fallback_adaptive_strategies(self) -> List[Dict[str, Any]]:
        """適応戦略のフォールバック"""
        return [
            {
                "strategy_type": "learning_pace",
                "trigger_conditions": ["進捗遅延", "理解困難"],
                "adaptations": ["学習速度調整", "追加説明提供"],
                "monitoring_metrics": ["完了率", "理解度"],
                "escalation_criteria": ["連続3日の遅延"]
            }
        ]
    
    def _fallback_risk_assessment(self) -> Dict[str, Any]:
        """リスク評価のフォールバック"""
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
                    "strategy": "優先順位付けとスケジュール管理",
                    "preventive_actions": ["時間ブロッキング"],
                    "contingency_plans": ["サポート強化"]
                }
            ],
            "monitoring_plan": {
                "early_warning_indicators": ["進捗遅延"],
                "monitoring_frequency": "週次",
                "escalation_procedures": ["メンター介入"]
            },
            "overall_risk_level": "medium"
        }
    
    def _fallback_diagnostic_analysis(self) -> Dict[str, Any]:
        """診断分析のフォールバック"""
        return {
            "current_state_assessment": "基本的な学習準備完了",
            "gap_analysis": "スキルギャップが特定されました",
            "root_cause_analysis": "経験不足が主要因",
            "readiness_assessment": "学習準備度は中程度",
            "priority_areas": ["基本スキル習得"],
            "success_probability": "中程度",
            "recommended_approach": "段階的学習",
            "timeline_estimation": "30-60日",
            "identified_gaps": ["基本知識", "実践経験"]
        }
    
    def _fallback_comprehensive_plan(self) -> Dict[str, Any]:
        """包括計画のフォールバック"""
        return {
            "executive_summary": "個別化された成長計画が作成されました",
            "key_insights": ["基本的な分析が完了", "改善領域が特定されました"],
            "personalized_roadmap": "段階的な学習アプローチで進行",
            "immediate_actions": ["基礎学習の開始", "定期的な進捗確認"],
            "success_predictors": ["継続的な学習", "定期的なフィードバック"],
            "potential_obstacles": ["時間管理", "モチベーション維持"],
            "recommended_resources": ["オンライン教材", "練習プロジェクト"],
            "follow_up_schedule": "週次進捗確認"
        }
    
    # 自律的エージェント用の追加メソッド
    
    async def analyze_content(self, prompt: str) -> str:
        """コンテンツ分析"""
        if not self.is_available():
            return "LLMが利用できません"
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは情報分析の専門家です。提供された情報を分析し、要点をまとめてください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.6
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Content analysis failed: {e}")
            return "分析に失敗しました"
    
    async def generate_questions(self, prompt: str) -> List[str]:
        """質問生成"""
        if not self.is_available():
            return ["基本的な質問"]
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは質問作成の専門家です。効果的な質問を生成してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            try:
                questions = json.loads(content)
                return questions if isinstance(questions, list) else [content]
            except json.JSONDecodeError:
                # 改行で分割して質問を抽出
                questions = [q.strip() for q in content.split('\n') if q.strip() and '?' in q]
                return questions[:5] if questions else ["基本的な質問"]
            
        except Exception as e:
            self.logger.error(f"Question generation failed: {e}")
            return ["基本的な質問"]
    
    async def generate_search_queries(self, prompt: str) -> Dict[str, List[str]]:
        """検索クエリ生成"""
        if not self.is_available():
            return {"web_search": ["基本検索"], "technical_search": ["技術検索"], "industry_search": ["業界検索"]}
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは検索クエリ作成の専門家です。効果的な検索クエリを生成してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=600,
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"web_search": ["基本検索"], "technical_search": ["技術検索"], "industry_search": ["業界検索"]}
            
        except Exception as e:
            self.logger.error(f"Search query generation failed: {e}")
            return {"web_search": ["基本検索"], "technical_search": ["技術検索"], "industry_search": ["業界検索"]}
    
    async def predict_challenges(self, prompt: str) -> Dict[str, Any]:
        """課題予測"""
        if not self.is_available():
            return {"predicted_challenges": ["学習ペースの維持"], "preventive_actions": ["定期的なチェックイン"]}
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは予測分析の専門家です。潜在的な課題を予測し、予防策を提案してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"predicted_challenges": ["学習ペースの維持"], "preventive_actions": ["定期的なチェックイン"]}
            
        except Exception as e:
            self.logger.error(f"Challenge prediction failed: {e}")
            return {"predicted_challenges": ["学習ペースの維持"], "preventive_actions": ["定期的なチェックイン"]}
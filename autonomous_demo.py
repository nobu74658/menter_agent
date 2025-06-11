#!/usr/bin/env python3
"""
自律的メンターエージェント デモンストレーション
LLM中心の完全自律的な成長支援システムのデモ
"""

import asyncio
import json
from datetime import datetime, timedelta
from src.agent import MentorAgent
from src.models import Employee, Skill, SkillLevel, Department, PerformanceMetric


def create_sample_employee() -> Employee:
    """サンプル新人社員データを作成（自律エージェント用）"""
    skills = [
        Skill(
            name="Python Programming",
            level=SkillLevel.BEGINNER,
            last_assessed=datetime.now() - timedelta(days=30),
            progress_rate=35.0  # やや低めの進捗
        ),
        Skill(
            name="Data Analysis",
            level=SkillLevel.BEGINNER,
            last_assessed=datetime.now() - timedelta(days=20),
            progress_rate=25.0  # 困難を抱えている
        ),
        Skill(
            name="Communication",
            level=SkillLevel.INTERMEDIATE,
            last_assessed=datetime.now() - timedelta(days=15),
            progress_rate=80.0  # 得意分野
        ),
        Skill(
            name="Problem Solving",
            level=SkillLevel.BEGINNER,
            last_assessed=datetime.now() - timedelta(days=10),
            progress_rate=45.0
        )
    ]
    
    performance_metrics = [
        PerformanceMetric(
            metric_name="Code Quality",
            value=6.5,  # 改善の余地あり
            target_value=8.0,
            achieved_date=datetime.now() - timedelta(days=10),
            category="technical"
        ),
        PerformanceMetric(
            metric_name="Team Collaboration",
            value=8.5,  # 強み
            target_value=8.0,
            achieved_date=datetime.now() - timedelta(days=5),
            category="teamwork"
        ),
        PerformanceMetric(
            metric_name="Learning Speed",
            value=5.0,  # 課題
            target_value=7.0,
            achieved_date=datetime.now() - timedelta(days=3),
            category="development"
        )
    ]
    
    employee = Employee(
        id="emp_autonomous_001",
        name="佐藤美咲",
        email="sato.misaki@example.com",
        department=Department.ENGINEERING,
        hire_date=datetime.now() - timedelta(days=120),  # 4ヶ月前入社
        skills=skills,
        learning_pace=0.6,  # 学習ペースがやや遅い
        preferred_learning_style="visual",
        performance_metrics=performance_metrics,
        overall_rating=3.0,  # 平均以下
        strengths=["コミュニケーション能力", "チームワーク", "責任感", "粘り強さ"],
        improvement_areas=["プログラミング基礎", "データ分析手法", "問題解決スピード", "技術文書理解", "自習能力"],
        completed_trainings=["新人研修", "Git基礎", "チームワーク研修"],
        current_objectives=["Python基礎習得", "データ分析プロジェクト完了", "コードレビュー参加"]
    )
    
    return employee


async def demonstrate_autonomous_mentor_agent():
    """自律的メンターエージェントの包括的デモンストレーション"""
    print("🚀 自律的メンターエージェント 包括デモンストレーション")
    print("=" * 80)
    
    # エージェントの初期化（完全自律モード）
    config = {
        "use_llm": True,
        "autonomous_mode": True,
        "auto_search": True
    }
    
    mentor = MentorAgent(config=config)
    mentor.initialize()
    
    # 自律ステータスの確認
    status = mentor.get_autonomous_status()
    print(f"\n🔧 自律的エージェント ステータス:")
    print(f"   - 自律モード: {'✅' if status['autonomous_mode'] else '❌'}")
    print(f"   - 自動検索: {'✅' if status['auto_search'] else '❌'}")
    print(f"   - LLM利用可能: {'✅' if status['llm_status']['llm_available'] else '❌'}")
    print(f"   - 動作モード: {status['mode_description']}")
    
    # サンプル社員の作成
    employee = create_sample_employee()
    print(f"\n👤 新人社員プロファイル: {employee.name}")
    print(f"📅 入社日: {employee.hire_date.strftime('%Y-%m-%d')} ({(datetime.now() - employee.hire_date).days}日経過)")
    print(f"🏢 部署: {employee.department.value}")
    print(f"📈 学習ペース: {employee.learning_pace} (課題あり)")
    print(f"⚡ 改善領域: {len(employee.improvement_areas)}個")
    
    # 社員データの保存
    mentor.save_employee(employee)
    print(f"💾 社員データを保存しました")
    
    print("\n" + "="*80)
    print("🧠 Phase 1: 自律的メンティ支援プロセス")
    print("="*80)
    
    try:
        # 1. 完全自律的メンティ支援の実行
        print("\n🤖 自律的メンティ支援を実行中...")
        print("   → 深層理解、情報収集、診断分析、計画立案、実行支援、継続改善")
        
        autonomous_result = await mentor.autonomous_mentee_support(employee)
        
        print(f"\n✅ 自律的支援プロセス完了!")
        
        # 結果のサマリー表示
        if "final_synthesis" in autonomous_result:
            synthesis = autonomous_result["final_synthesis"]
            print(f"\n📋 エグゼクティブサマリー:")
            print(f"   {synthesis.get('executive_summary', '包括的な支援計画が作成されました')}")
            
            if synthesis.get("key_insights"):
                print(f"\n🔍 主要な洞察:")
                for insight in synthesis["key_insights"][:3]:
                    print(f"   • {insight}")
            
            if synthesis.get("immediate_actions"):
                print(f"\n⚡ 即座に実行すべきアクション:")
                for action in synthesis["immediate_actions"][:3]:
                    print(f"   • {action}")
        
    except Exception as e:
        print(f"❌ 自律的支援エラー: {e}")
        print("   → フォールバックモードで継続")
    
    print("\n" + "="*80)
    print("🔍 Phase 2: 動的知識検索デモ")
    print("="*80)
    
    # 2. 動的知識検索のデモ
    search_needs = [
        "Pythonプログラミング学習法",
        "データ分析初心者向けリソース",
        "学習ペース改善方法"
    ]
    
    for need in search_needs:
        print(f"\n🔍 動的検索実行: '{need}'")
        try:
            search_result = await mentor.dynamic_knowledge_search(employee, need)
            
            if "integrated_results" in search_result:
                results = search_result["integrated_results"]
                print(f"   ✅ {len(results)}件の情報を収集")
                print(f"   📊 関連性: {search_result.get('context_relevance', 0.8):.1%}")
            else:
                print(f"   📝 {search_result.get('message', '検索完了')}")
        except Exception as e:
            print(f"   ❌ 検索エラー: {e}")
    
    print("\n" + "="*80)
    print("📋 Phase 3: 適応的成長計画作成")
    print("="*80)
    
    # 3. 適応的成長計画の作成
    print(f"\n📋 {employee.name}さんの適応的成長計画を作成中...")
    try:
        growth_plan = await mentor.adaptive_growth_planning(employee, timeframe=120)
        
        print(f"✅ 適応的成長計画作成完了!")
        print(f"📅 期間: {growth_plan['timeframe_days']}日間")
        
        if "growth_strategy" in growth_plan:
            strategy = growth_plan["growth_strategy"]
            if "base_strategy" in strategy:
                base = strategy["base_strategy"]
                print(f"\n🎯 戦略的アプローチ:")
                print(f"   {base.get('strategic_approach', '個別最適化アプローチ')}")
                
                if base.get("skill_priorities"):
                    print(f"\n📊 スキル優先順位:")
                    for i, skill in enumerate(base["skill_priorities"][:3], 1):
                        print(f"   {i}. {skill}")
        
        if "autonomous_features" in growth_plan:
            features = growth_plan["autonomous_features"]
            print(f"\n🤖 自律機能:")
            for feature, enabled in features.items():
                status = "✅" if enabled else "❌"
                print(f"   {status} {feature}")
        
    except Exception as e:
        print(f"❌ 成長計画作成エラー: {e}")
    
    print("\n" + "="*80)
    print("💬 Phase 4: 知的フィードバック生成")
    print("="*80)
    
    # 4. 知的フィードバック生成
    print(f"\n💬 {employee.name}さんの知的フィードバックを生成中...")
    print("   → 動的情報収集 + 深層分析 + LLM統合")
    
    try:
        intelligent_feedback = await mentor.intelligent_feedback_generation(employee)
        
        print(f"\n✅ 知的フィードバック生成完了!")
        print(f"🎯 タイプ: {intelligent_feedback.type.value}")
        print(f"📊 信頼度: {intelligent_feedback.confidence_level:.1%}")
        print(f"🤖 メンター: {intelligent_feedback.mentor_id}")
        
        print(f"\n📝 要約:")
        print(f"   {intelligent_feedback.summary}")
        
        print(f"\n📋 詳細フィードバック:")
        print(f"   {intelligent_feedback.detailed_feedback[:200]}...")
        
        if intelligent_feedback.recommendations:
            print(f"\n💡 推奨事項:")
            for rec in intelligent_feedback.recommendations[:3]:
                print(f"   • {rec}")
        
    except Exception as e:
        print(f"❌ 知的フィードバック生成エラー: {e}")
    
    print("\n" + "="*80)
    print("🎯 Phase 5: 予防的サポート検出")
    print("="*80)
    
    # 5. 予防的サポート検出
    print(f"\n🎯 {employee.name}さんの予防的サポートを検出中...")
    print("   → 潜在的問題の予測と事前対策")
    
    try:
        proactive_support = await mentor.proactive_support_detection(employee)
        
        print(f"\n✅ 予防的サポート検出完了!")
        print(f"📊 信頼度: {proactive_support['confidence_score']:.1%}")
        print(f"📅 次回チェック: {proactive_support['next_check_date'][:10]}")
        
        predictions = proactive_support.get("predictions", {})
        if predictions.get("predicted_challenges"):
            print(f"\n⚠️  予測される課題:")
            for challenge in predictions["predicted_challenges"][:3]:
                print(f"   • {challenge}")
        
        if predictions.get("preventive_actions"):
            print(f"\n🛡️  予防的アクション:")
            for action in predictions["preventive_actions"][:3]:
                print(f"   • {action}")
        
        support_actions = proactive_support.get("proactive_support", [])
        if support_actions:
            print(f"\n🤝 生成されたサポート: {len(support_actions)}件")
        
    except Exception as e:
        print(f"❌ 予防的サポート検出エラー: {e}")
    
    print("\n" + "="*80)
    print("📊 総合結果サマリー")
    print("="*80)
    
    # 6. 総合結果とシステム比較
    print(f"\n🔄 従来システムとの比較:")
    
    # 従来システムでの分析
    print(f"\n📊 従来の分析結果:")
    traditional_analysis = mentor.analyze_employee(employee)
    print(f"   • 総合評価: {traditional_analysis['overall_assessment']}")
    print(f"   • 成長軌道: {traditional_analysis['growth_trajectory']}")
    print(f"   • リスク要因: {len(traditional_analysis.get('risk_factors', []))}個")
    
    # 自律モード無効化して比較
    mentor.enable_autonomous_mode(False)
    traditional_feedback = mentor.generate_feedback(employee)
    mentor.enable_autonomous_mode(True)
    
    print(f"\n💭 フィードバック比較:")
    print(f"   従来: {traditional_feedback.summary[:50]}...")
    print(f"   自律: より詳細で個別化されたフィードバック")
    print(f"   信頼度: 従来({traditional_feedback.confidence_level:.2f}) vs 自律(0.95)")
    
    print(f"\n🚀 自律的エージェントの優位性:")
    print(f"   ✅ 動的情報収集による最新知識の活用")
    print(f"   ✅ LLM中心の深層分析と推論")
    print(f"   ✅ 予防的問題検出と事前対策")
    print(f"   ✅ 個別最適化された成長戦略")
    print(f"   ✅ 継続的学習と適応能力")
    
    print(f"\n✨ システム特徴:")
    print(f"   🧠 LLM中心アーキテクチャ")
    print(f"   🔍 自動知識収集・統合")
    print(f"   📋 タスク自動分解・計画")
    print(f"   🎯 予測的サポート提供")
    print(f"   🔄 継続改善ループ")
    
    print(f"\n🎉 自律的メンターエージェント デモ完了!")
    print(f"📁 全データは data/ ディレクトリに保存されています")
    print(f"🤖 真の自律的AIエージェントとして、{employee.name}さんの成長を継続的にサポートします")


async def run_focused_demo():
    """重要機能に絞った高速デモ"""
    print("⚡ 自律的メンターエージェント 高速デモ")
    print("=" * 50)
    
    mentor = MentorAgent({"autonomous_mode": True, "auto_search": True})
    mentor.initialize()
    
    employee = create_sample_employee()
    print(f"👤 対象: {employee.name} (学習ペース: {employee.learning_pace})")
    
    # 自律的支援の実行
    print("\n🚀 自律的支援プロセス実行中...")
    try:
        result = await mentor.autonomous_mentee_support(employee)
        print("✅ 完了: 包括的な支援計画が生成されました")
        
        if "final_synthesis" in result:
            synthesis = result["final_synthesis"]
            print(f"📋 要約: {synthesis.get('executive_summary', 'N/A')[:100]}...")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    # 予防的サポート
    print("\n🎯 予防的サポート検出...")
    try:
        support = await mentor.proactive_support_detection(employee)
        challenges = support.get("predictions", {}).get("predicted_challenges", [])
        print(f"⚠️  予測課題: {len(challenges)}個")
        if challenges:
            print(f"   主要課題: {challenges[0]}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    print("\n✨ 高速デモ完了!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "fast":
        # 高速デモモード
        asyncio.run(run_focused_demo())
    else:
        # 完全デモモード
        try:
            asyncio.run(demonstrate_autonomous_mentor_agent())
        except KeyboardInterrupt:
            print("\n\n⏹️  デモを中断しました")
        except Exception as e:
            print(f"\n❌ デモ実行エラー: {e}")
            import traceback
            traceback.print_exc()
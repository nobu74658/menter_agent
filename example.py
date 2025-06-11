#!/usr/bin/env python3
"""
メンターエージェントのデモンストレーション
新人社員のサンプルデータを使用してエージェントの機能を実演
"""

from datetime import datetime, timedelta
from src.agent import MentorAgent
from src.models import Employee, Skill, SkillLevel, Department, PerformanceMetric

def create_sample_employee() -> Employee:
    """サンプル新人社員データを作成"""
    skills = [
        Skill(
            name="Python Programming",
            level=SkillLevel.BEGINNER,
            last_assessed=datetime.now() - timedelta(days=30),
            progress_rate=45.0
        ),
        Skill(
            name="Communication",
            level=SkillLevel.INTERMEDIATE,
            last_assessed=datetime.now() - timedelta(days=15),
            progress_rate=72.0
        ),
        Skill(
            name="Project Management",
            level=SkillLevel.BEGINNER,
            last_assessed=datetime.now() - timedelta(days=20),
            progress_rate=30.0
        )
    ]
    
    performance_metrics = [
        PerformanceMetric(
            metric_name="Code Quality",
            value=7.5,
            target_value=8.0,
            achieved_date=datetime.now() - timedelta(days=10),
            category="technical"
        ),
        PerformanceMetric(
            metric_name="Team Collaboration",
            value=8.2,
            target_value=8.0,
            achieved_date=datetime.now() - timedelta(days=5),
            category="teamwork"
        )
    ]
    
    employee = Employee(
        id="emp_001",
        name="田中太郎",
        email="tanaka@example.com",
        department=Department.ENGINEERING,
        hire_date=datetime.now() - timedelta(days=90),
        skills=skills,
        learning_pace=0.8,
        preferred_learning_style="visual",
        performance_metrics=performance_metrics,
        overall_rating=3.5,
        strengths=["学習が早い", "チームプレイヤー", "細部への注意力"],
        improvement_areas=["技術文書作成", "時間管理", "プレゼンテーション"],
        completed_trainings=["新人研修", "Git基礎"],
        current_objectives=["Python認定資格取得", "コードレビュースキル向上"]
    )
    
    return employee

def demonstrate_mentor_agent():
    """メンターエージェントのデモンストレーション（LLM統合版）"""
    print("🤖 メンターエージェント デモンストレーション（LLM統合版）")
    print("=" * 60)
    
    # エージェントの初期化
    mentor = MentorAgent()
    mentor.initialize()
    
    # LLMステータスの確認
    llm_status = mentor.get_llm_status()
    print(f"\n🔧 LLMステータス:")
    print(f"   - LLM利用可能: {'✅' if llm_status['llm_available'] else '❌'}")
    print(f"   - LLM有効: {'✅' if llm_status['llm_enabled'] else '❌'}")
    print(f"   - 動作モード: {llm_status['mode']}")
    
    # サンプル社員の作成
    employee = create_sample_employee()
    print(f"\n👤 新人社員: {employee.name}")
    print(f"📅 入社日: {employee.hire_date.strftime('%Y-%m-%d')}")
    print(f"🏢 部署: {employee.department.value}")
    print(f"📈 学習ペース: {employee.learning_pace}")
    
    # 社員の保存
    mentor.save_employee(employee)
    print(f"💾 社員データを保存しました")
    
    # 1. 社員分析
    print(f"\n📊 社員分析結果:")
    print("-" * 30)
    analysis = mentor.analyze_employee(employee)
    print(f"総合評価: {analysis['overall_assessment']}")
    print(f"成長軌道: {analysis['growth_trajectory']}")
    print(f"スキル数: {analysis['skill_analysis']['total_skills']}")
    print(f"平均進捗: {analysis['skill_analysis']['average_progress']:.1f}%")
    
    if analysis['risk_factors']:
        print(f"⚠️  リスク要因:")
        for risk in analysis['risk_factors']:
            print(f"   - {risk}")
    
    # 2. フィードバック生成
    print(f"\n💬 個別フィードバック:")
    print("-" * 30)
    feedback = mentor.generate_feedback(employee)
    print(f"タイプ: {feedback.type.value}")
    print(f"カテゴリ: {feedback.category}")
    print(f"要約: {feedback.summary}")
    print(f"詳細: {feedback.detailed_feedback}")
    print(f"インパクトスコア: {feedback.impact_score}/10")
    
    if feedback.action_items:
        print(f"\n📋 アクションアイテム:")
        for i, item in enumerate(feedback.action_items[:3], 1):
            print(f"   {i}. {item.description}")
            print(f"      期限: {item.due_date.strftime('%Y-%m-%d')}")
            print(f"      優先度: {item.priority.value}")
    
    # 3. 成長計画作成
    print(f"\n🎯 成長計画 (90日間):")
    print("-" * 30)
    growth_plan = mentor.create_growth_plan(employee, timeframe=90)
    print(f"期間: {growth_plan['timeframe_days']}日間")
    
    if growth_plan['objectives']:
        print(f"\n目標:")
        for obj in growth_plan['objectives']:
            print(f"   - {obj['area']}: {obj['current_state']} → {obj['target_state']} (優先度: {obj['priority']})")
    
    if growth_plan['learning_path']:
        print(f"\n学習パス:")
        for step in growth_plan['learning_path']:
            print(f"   Step {step['step']}: {step['skill']} ({step['duration_days']}日)")
    
    # 4. 進捗トラッキング
    print(f"\n📈 進捗トラッキング:")
    print("-" * 30)
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    growth_record = mentor.track_progress(employee, start_date, end_date)
    
    print(f"期間: {start_date.strftime('%Y-%m-%d')} ～ {end_date.strftime('%Y-%m-%d')}")
    print(f"総合成長スコア: {growth_record.overall_growth_score}/10")
    print(f"成長トレンド: {growth_record.growth_trend.value}")
    
    if growth_record.key_achievements:
        print(f"\n🏆 主な成果:")
        for achievement in growth_record.key_achievements:
            print(f"   - {achievement}")
    
    if growth_record.challenges_faced:
        print(f"\n⚡ 直面した課題:")
        for challenge in growth_record.challenges_faced:
            print(f"   - {challenge}")
    
    # 5. サポート提供（LLM強化）
    print(f"\n🤝 自律的サポート例（LLM強化）:")
    print("-" * 40)
    
    support_types = ["skill_gap", "motivation", "communication"]
    for support_type in support_types:
        support_response = mentor.provide_support(employee, support_type)
        
        support_type_jp = {
            "skill_gap": "スキルギャップ",
            "motivation": "モチベーション", 
            "communication": "コミュニケーション"
        }.get(support_type, support_type)
        
        print(f"\n{support_type_jp}サポート:")
        
        # LLMメッセージがある場合は表示
        if support_response.get('support_message'):
            print(f"   💬 AIメッセージ: {support_response['support_message'][:100]}...")
            if support_response.get('message_source') == 'llm':
                print(f"   📝 ソース: LLM生成")
        
        # ルールベースのアクション
        print(f"   🔧 サポートアクション:")
        for action in support_response['support_provided'][:2]:
            print(f"      - {action}")
    
    # 6. LLMとルールベースの比較（利用可能な場合）
    if llm_status['llm_available']:
        print(f"\n🔄 LLMとルールベースの比較:")
        print("-" * 40)
        
        # ルールベースモードでフィードバック生成
        mentor.toggle_llm_mode(False)
        rule_feedback = mentor.generate_feedback(employee)
        
        # LLMモードでフィードバック生成
        mentor.toggle_llm_mode(True)
        llm_feedback = mentor.generate_feedback(employee)
        
        print(f"ルールベース: {rule_feedback.summary}")
        print(f"LLM生成: {llm_feedback.summary}")
        print(f"信頼度比較: ルール({rule_feedback.confidence_level}) vs LLM({llm_feedback.confidence_level})")
    
    print(f"\n✅ LLM統合デモンストレーション完了!")
    print(f"📁 データは data/ ディレクトリに保存されています")
    print(f"🎯 LLM機能により、より自然で個別化されたフィードバックを提供しています")

if __name__ == "__main__":
    try:
        demonstrate_mentor_agent()
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
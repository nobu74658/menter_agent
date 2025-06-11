#!/usr/bin/env python3
"""
メンターエージェントのメインエントリーポイント
新人社員の教育支援AIシステムのデモンストレーション
"""

import json
from datetime import datetime
from pathlib import Path

from src.agent import MentorAgent
from src.utils import SampleDataGenerator
from src.models import Department


def demonstrate_mentor_agent():
    """メンターエージェントのデモンストレーション"""
    print("=== メンターエージェント デモンストレーション ===\n")
    
    # エージェントの初期化
    print("1. メンターエージェントを初期化中...")
    mentor = MentorAgent()
    
    # サンプルデータの生成
    print("2. サンプル新人社員データを生成中...")
    data_generator = SampleDataGenerator()
    
    # 多様なシナリオの社員を生成
    employees = data_generator.generate_diverse_scenarios()
    
    print(f"   - {len(employees)}人の新人社員データを生成しました\n")
    
    # 各社員に対してメンタリングを実行
    for i, employee in enumerate(employees, 1):
        print(f"=== 社員 {i}: {employee.name} ({employee.department.value}) ===")
        
        # 社員データを保存
        mentor.save_employee(employee)
        
        # 1. 分析の実行
        print("📊 分析実行中...")
        analysis = mentor.analyze_employee(employee)
        print(f"   - 総合評価: {analysis['overall_assessment']}")
        print(f"   - 成長軌道: {analysis['growth_trajectory']}")
        print(f"   - 平均スキル進捗: {analysis['skill_analysis']['average_progress']:.1f}%")
        
        if analysis['risk_factors']:
            print(f"   - リスク要因: {', '.join(analysis['risk_factors'])}")
        
        # 2. フィードバックの生成
        print("\n💬 フィードバック生成中...")
        feedback = mentor.generate_feedback(employee)
        print(f"   - タイプ: {feedback.type.value}")
        print(f"   - カテゴリ: {feedback.category}")
        print(f"   - インパクトスコア: {feedback.impact_score:.1f}/10")
        print(f"   - 要約: {feedback.summary}")
        
        if feedback.action_items:
            print(f"   - アクションアイテム数: {len(feedback.action_items)}")
            for action in feedback.action_items[:2]:
                print(f"     • {action.description}")
        
        # 3. 成長計画の作成
        print("\n📈 成長計画作成中...")
        growth_plan = mentor.create_growth_plan(employee)
        print(f"   - 期間: {growth_plan['timeframe_days']}日間")
        print(f"   - 主要目標数: {len(growth_plan['objectives'])}")
        print(f"   - マイルストーン数: {len(growth_plan['milestones'])}")
        
        if growth_plan['objectives']:
            print("   - 主要目標:")
            for obj in growth_plan['objectives'][:3]:
                print(f"     • {obj}")
        
        # 4. 進捗トラッキング
        print("\n📋 進捗トラッキング実行中...")
        start_date = employee.hire_date
        end_date = datetime.now()
        growth_record = mentor.track_progress(employee, start_date, end_date)
        
        print(f"   - 成長スコア: {growth_record.overall_growth_score:.1f}/10")
        print(f"   - 成長トレンド: {growth_record.growth_trend.value}")
        print(f"   - スキル進捗記録数: {len(growth_record.skill_progress)}")
        
        if growth_record.key_achievements:
            print("   - 主要な成果:")
            for achievement in growth_record.key_achievements[:2]:
                print(f"     • {achievement}")
        
        # 5. 自律的サポート
        print("\n🤝 自律的サポート提供中...")
        
        # リスク要因に基づいてサポートを提供
        if analysis['risk_factors']:
            if "slow learning pace" in str(analysis['risk_factors']).lower():
                support = mentor.provide_support(employee, "motivation")
                print("   - サポートタイプ: モチベーション向上")
            elif "multiple improvement areas" in str(analysis['risk_factors']).lower():
                support = mentor.provide_support(employee, "skill_gap")
                print("   - サポートタイプ: スキルギャップ対応")
            else:
                support = mentor.provide_support(employee, "general")
                print("   - サポートタイプ: 一般的サポート")
        else:
            support = mentor.provide_support(employee, "general")
            print("   - サポートタイプ: 一般的サポート")
        
        if support['support_provided']:
            print("   - 提供されたサポート:")
            for sup in support['support_provided'][:3]:
                print(f"     • {sup}")
        
        print("\n" + "="*50 + "\n")
    
    # サマリー統計
    print("=== サマリー統計 ===")
    
    # 部署別分布
    dept_counts = {}
    total_growth_score = 0
    
    for employee in employees:
        dept = employee.department.value
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
        total_growth_score += mentor.calculate_growth_score(employee)
    
    print("部署別分布:")
    for dept, count in dept_counts.items():
        print(f"  - {dept}: {count}人")
    
    avg_growth_score = total_growth_score / len(employees)
    print(f"\n平均成長スコア: {avg_growth_score:.1f}/10")
    
    # 保存されたファイル数の確認
    data_dir = Path("data")
    employee_files = list((data_dir / "employees").glob("*.json"))
    feedback_files = list((data_dir / "feedbacks").glob("*.json"))
    
    print(f"\n保存されたデータ:")
    print(f"  - 社員ファイル: {len(employee_files)}個")
    print(f"  - フィードバックファイル: {len(feedback_files)}個")
    
    print("\n✅ デモンストレーション完了!")
    print("   生成されたデータは data/ ディレクトリに保存されました。")


def demonstrate_specific_scenario():
    """特定のシナリオでのデモンストレーション"""
    print("\n=== 特定シナリオ: 苦戦している新人への対応 ===\n")
    
    mentor = MentorAgent()
    data_generator = SampleDataGenerator()
    
    # 苦戦している新人を生成
    struggling_employee = data_generator.generate_employee(
        department=Department.ENGINEERING,
        experience_level="struggling"
    )
    
    print(f"社員: {struggling_employee.name}")
    print(f"部署: {struggling_employee.department.value}")
    print(f"学習ペース: {struggling_employee.learning_pace}")
    print(f"改善が必要な領域: {len(struggling_employee.improvement_areas)}個")
    
    # 詳細分析
    analysis = mentor.analyze_employee(struggling_employee)
    print(f"\n総合評価: {analysis['overall_assessment']}")
    print(f"リスク要因: {analysis['risk_factors']}")
    
    # 集中的サポートの提供
    print("\n🚨 集中的サポートプログラムの開始")
    
    # スキルギャップサポート
    skill_support = mentor.provide_support(struggling_employee, "skill_gap")
    print("\nスキルギャップサポート:")
    for support in skill_support['support_provided']:
        print(f"  • {support}")
    
    # モチベーションサポート
    motivation_support = mentor.provide_support(struggling_employee, "motivation")
    print("\nモチベーションサポート:")
    for support in motivation_support['support_provided']:
        print(f"  • {support}")
    
    # カスタマイズされた成長計画
    growth_plan = mentor.create_growth_plan(struggling_employee, timeframe=60)  # 2ヶ月集中プログラム
    print(f"\n📚 カスタマイズされた60日間集中プログラム")
    print(f"主要目標:")
    for obj in growth_plan['objectives']:
        print(f"  • {obj}")
    
    print(f"\nサポートメカニズム:")
    for mechanism in growth_plan['support_mechanisms']:
        print(f"  • {mechanism}")
    
    print("\n✅ 集中サポートプログラム設計完了!")


if __name__ == "__main__":
    try:
        # メインデモンストレーション
        demonstrate_mentor_agent()
        
        # 特定シナリオのデモ
        demonstrate_specific_scenario()
        
    except KeyboardInterrupt:
        print("\n\n❌ デモンストレーションが中断されました。")
    except Exception as e:
        print(f"\n\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.agent import MentorAgent
from src.models import Employee, Department, SkillLevel, Skill
from src.utils import SampleDataGenerator


class TestMentorAgent(unittest.TestCase):
    """メンターエージェントのテストケース"""
    
    def setUp(self):
        """テストのセットアップ"""
        self.mentor = MentorAgent()
        self.data_generator = SampleDataGenerator()
        
        # テスト用の社員データ
        self.test_employee = Employee(
            id="test_001",
            name="Test Employee",
            email="test@company.com",
            department=Department.ENGINEERING,
            hire_date=datetime.now() - timedelta(days=90),
            skills=[
                Skill(
                    name="Python",
                    level=SkillLevel.BEGINNER,
                    last_assessed=datetime.now(),
                    progress_rate=45.0
                ),
                Skill(
                    name="JavaScript",
                    level=SkillLevel.INTERMEDIATE,
                    last_assessed=datetime.now(),
                    progress_rate=75.0
                )
            ],
            learning_pace=1.2,
            preferred_learning_style="hands-on",
            strengths=["Quick learner", "Good problem solver"],
            improvement_areas=["Time management", "Communication"],
            current_objectives=["Improve Python skills", "Learn React"]
        )
    
    def test_agent_initialization(self):
        """エージェントの初期化テスト"""
        self.assertIsNotNone(self.mentor)
        self.assertIsNotNone(self.mentor.analysis_service)
        self.assertIsNotNone(self.mentor.feedback_service)
        self.assertIsNotNone(self.mentor.growth_service)
    
    def test_analyze_employee(self):
        """社員分析機能のテスト"""
        analysis = self.mentor.analyze_employee(self.test_employee)
        
        self.assertIn("employee_id", analysis)
        self.assertIn("overall_assessment", analysis)
        self.assertIn("skill_analysis", analysis)
        self.assertIn("growth_trajectory", analysis)
        self.assertIn("recommendations", analysis)
        
        self.assertEqual(analysis["employee_id"], "test_001")
        self.assertIsInstance(analysis["skill_analysis"], dict)
        self.assertIsInstance(analysis["recommendations"], list)
    
    def test_generate_feedback(self):
        """フィードバック生成のテスト"""
        feedback = self.mentor.generate_feedback(self.test_employee)
        
        self.assertEqual(feedback.employee_id, "test_001")
        self.assertIsNotNone(feedback.type)
        self.assertIsNotNone(feedback.category)
        self.assertTrue(len(feedback.summary) > 0)
        self.assertTrue(0 <= feedback.impact_score <= 10)
        self.assertTrue(0 <= feedback.confidence_level <= 1)
    
    def test_create_growth_plan(self):
        """成長計画作成のテスト"""
        growth_plan = self.mentor.create_growth_plan(self.test_employee, timeframe=60)
        
        self.assertEqual(growth_plan["employee_id"], "test_001")
        self.assertEqual(growth_plan["timeframe_days"], 60)
        self.assertIn("objectives", growth_plan)
        self.assertIn("milestones", growth_plan)
        self.assertIn("learning_path", growth_plan)
        
        self.assertIsInstance(growth_plan["objectives"], list)
        self.assertIsInstance(growth_plan["milestones"], list)
    
    def test_track_progress(self):
        """進捗トラッキングのテスト"""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        growth_record = self.mentor.track_progress(self.test_employee, start_date, end_date)
        
        self.assertEqual(growth_record.employee_id, "test_001")
        self.assertEqual(growth_record.period_start, start_date)
        self.assertEqual(growth_record.period_end, end_date)
        self.assertTrue(0 <= growth_record.overall_growth_score <= 10)
        self.assertIsNotNone(growth_record.growth_trend)
    
    def test_provide_support(self):
        """サポート提供のテスト"""
        support_types = ["skill_gap", "motivation", "communication", "workload"]
        
        for support_type in support_types:
            support = self.mentor.provide_support(self.test_employee, support_type)
            
            self.assertEqual(support["employee_id"], "test_001")
            self.assertEqual(support["issue_type"], support_type)
            self.assertIn("support_provided", support)
            self.assertIn("follow_up_actions", support)
            self.assertIn("resources", support)
            
            self.assertIsInstance(support["support_provided"], list)
            self.assertTrue(len(support["support_provided"]) > 0)
    
    def test_calculate_growth_score(self):
        """成長スコア計算のテスト"""
        score = self.mentor.calculate_growth_score(self.test_employee)
        
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 10)
    
    def test_assess_learning_needs(self):
        """学習ニーズ評価のテスト"""
        needs = self.mentor.assess_learning_needs(self.test_employee)
        
        self.assertIsInstance(needs, list)
        # Python スキルが低い進捗なので、改善ニーズに含まれるはず
        python_needs = [need for need in needs if "Python" in need]
        self.assertTrue(len(python_needs) > 0)
    
    def test_employee_save_and_load(self):
        """社員データの保存と読み込みのテスト"""
        # 保存
        self.mentor.save_employee(self.test_employee)
        
        # 読み込み
        loaded_employee = self.mentor.load_employee("test_001")
        
        self.assertIsNotNone(loaded_employee)
        self.assertEqual(loaded_employee.id, "test_001")
        self.assertEqual(loaded_employee.name, "Test Employee")
        self.assertEqual(len(loaded_employee.skills), 2)


class TestSampleDataGenerator(unittest.TestCase):
    """サンプルデータ生成器のテストケース"""
    
    def setUp(self):
        self.generator = SampleDataGenerator()
    
    def test_generate_employee(self):
        """社員データ生成のテスト"""
        employee = self.generator.generate_employee(
            department=Department.ENGINEERING,
            experience_level="entry"
        )
        
        self.assertIsInstance(employee, Employee)
        self.assertEqual(employee.department, Department.ENGINEERING)
        self.assertTrue(len(employee.skills) > 0)
        self.assertTrue(len(employee.strengths) > 0)
        self.assertTrue(len(employee.improvement_areas) > 0)
        self.assertTrue(0.5 <= employee.learning_pace <= 2.0)
    
    def test_generate_employee_batch(self):
        """社員データバッチ生成のテスト"""
        employees = self.generator.generate_employee_batch(count=5)
        
        self.assertEqual(len(employees), 5)
        for employee in employees:
            self.assertIsInstance(employee, Employee)
            self.assertTrue(len(employee.id) > 0)
            self.assertTrue(len(employee.name) > 0)
    
    def test_generate_diverse_scenarios(self):
        """多様なシナリオ生成のテスト"""
        employees = self.generator.generate_diverse_scenarios()
        
        self.assertTrue(len(employees) > 0)
        
        # 異なる部署が含まれていることを確認
        departments = set(emp.department for emp in employees)
        self.assertTrue(len(departments) > 1)
        
        # 異なる学習ペースが含まれていることを確認
        learning_paces = [emp.learning_pace for emp in employees]
        self.assertTrue(max(learning_paces) > min(learning_paces))


class TestIntegration(unittest.TestCase):
    """統合テストケース"""
    
    def setUp(self):
        self.mentor = MentorAgent()
        self.generator = SampleDataGenerator()
    
    def test_full_mentoring_workflow(self):
        """完全なメンタリングワークフローのテスト"""
        # 1. 社員データ生成
        employee = self.generator.generate_employee(
            department=Department.SALES,
            experience_level="struggling"
        )
        
        # 2. 分析実行
        analysis = self.mentor.analyze_employee(employee)
        self.assertIsNotNone(analysis)
        
        # 3. フィードバック生成
        feedback = self.mentor.generate_feedback(employee)
        self.assertIsNotNone(feedback)
        
        # 4. 成長計画作成
        growth_plan = self.mentor.create_growth_plan(employee)
        self.assertIsNotNone(growth_plan)
        
        # 5. 進捗トラッキング
        start_date = employee.hire_date
        end_date = datetime.now()
        growth_record = self.mentor.track_progress(employee, start_date, end_date)
        self.assertIsNotNone(growth_record)
        
        # 6. サポート提供
        support = self.mentor.provide_support(employee, "skill_gap")
        self.assertIsNotNone(support)
        
        # 全てのコンポーネントが正常に動作することを確認
        self.assertTrue(True)  # ここまで到達すれば成功
    
    def test_multiple_employees_processing(self):
        """複数社員の処理テスト"""
        employees = self.generator.generate_employee_batch(count=3)
        
        for employee in employees:
            # 各社員に対して基本的な処理を実行
            analysis = self.mentor.analyze_employee(employee)
            feedback = self.mentor.generate_feedback(employee)
            
            self.assertIsNotNone(analysis)
            self.assertIsNotNone(feedback)
            self.assertEqual(feedback.employee_id, employee.id)


if __name__ == "__main__":
    unittest.main()
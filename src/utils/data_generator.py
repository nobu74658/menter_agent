from typing import List, Dict, Any
from datetime import datetime, timedelta
import random
import uuid

from ..models import (
    Employee, Skill, PerformanceMetric, 
    SkillLevel, Department
)


class SampleDataGenerator:
    """サンプルデータ生成器"""
    
    def __init__(self):
        self.first_names = [
            "Alex", "Blake", "Casey", "Drew", "Ellis", "Finley", "Gray", "Harley",
            "Indigo", "Jessie", "Kelly", "Lane", "Morgan", "Nico", "Oakley", "Parker",
            "Quinn", "River", "Sage", "Taylor", "Uma", "Val", "Winter", "Xen", "Yale", "Zen"
        ]
        
        self.last_names = [
            "Anderson", "Brown", "Chen", "Davis", "Evans", "Fisher", "Garcia", "Harris",
            "Johnson", "Kim", "Lee", "Martinez", "Nelson", "O'Connor", "Patel", "Quinn",
            "Rodriguez", "Smith", "Taylor", "Umeda", "Vang", "Wilson", "Xavier", "Young", "Zhang"
        ]
        
        self.skill_names = {
            Department.ENGINEERING: [
                "Python", "JavaScript", "SQL", "Docker", "AWS", "React", "Node.js", 
                "Machine Learning", "System Design", "Testing", "DevOps", "API Design"
            ],
            Department.SALES: [
                "CRM Management", "Lead Generation", "Negotiation", "Product Knowledge",
                "Customer Relations", "Presentation Skills", "Market Analysis", "Closing Techniques"
            ],
            Department.MARKETING: [
                "Content Marketing", "Social Media", "SEO", "Analytics", "Email Marketing",
                "Brand Management", "Campaign Management", "Graphic Design"
            ],
            Department.HR: [
                "Recruiting", "Employee Relations", "Training & Development", "Compliance",
                "Performance Management", "Compensation", "Benefits Administration", "HRIS"
            ],
            Department.FINANCE: [
                "Financial Analysis", "Accounting", "Excel", "Financial Modeling",
                "Budgeting", "Reporting", "Tax Preparation", "Auditing"
            ],
            Department.OPERATIONS: [
                "Process Management", "Quality Control", "Supply Chain", "Project Management",
                "Logistics", "Inventory Management", "Vendor Relations", "Process Improvement"
            ]
        }
        
        self.personality_traits = [
            "adaptability", "communication", "teamwork", "leadership", "creativity",
            "problem_solving", "attention_to_detail", "time_management", "initiative", "reliability"
        ]
        
        self.strengths_pool = [
            "Strong analytical thinking", "Excellent communication skills", "Natural leadership abilities",
            "Creative problem solving", "Detail-oriented approach", "Strong technical aptitude",
            "Collaborative team player", "Quick learner", "Reliable and consistent",
            "Innovative mindset", "Customer-focused", "Results-driven"
        ]
        
        self.improvement_areas_pool = [
            "Time management", "Public speaking", "Technical documentation", "Cross-functional collaboration",
            "Strategic thinking", "Data analysis", "Project management", "Delegation skills",
            "Conflict resolution", "Presentation skills", "Networking", "Industry knowledge"
        ]
        
        self.training_modules = [
            "New Employee Orientation", "Technical Skills Bootcamp", "Communication Workshop",
            "Leadership Fundamentals", "Customer Service Excellence", "Project Management Basics",
            "Data Analysis for Beginners", "Agile Methodologies", "Digital Marketing Essentials",
            "Financial Literacy", "Diversity and Inclusion", "Safety Training"
        ]
    
    def generate_employee(self, department: Department = None, 
                         experience_level: str = "entry") -> Employee:
        """新人社員のデータを生成"""
        
        if department is None:
            department = random.choice(list(Department))
        
        employee_id = str(uuid.uuid4())[:8]
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        
        # 基本情報
        hire_date = datetime.now() - timedelta(days=random.randint(30, 365))
        
        # スキル生成
        skills = self._generate_skills(department, experience_level)
        
        # パフォーマンス指標生成
        performance_metrics = self._generate_performance_metrics(department)
        
        # 学習特性
        learning_pace = random.uniform(0.5, 2.0)
        if experience_level == "fast_learner":
            learning_pace = random.uniform(1.2, 2.0)
        elif experience_level == "struggling":
            learning_pace = random.uniform(0.3, 0.8)
        
        # 特性とエリア
        strengths = random.sample(self.strengths_pool, random.randint(2, 4))
        improvement_areas = random.sample(self.improvement_areas_pool, random.randint(2, 5))
        
        # パーソナリティ特性
        personality_traits = {
            trait: random.uniform(0.2, 1.0) 
            for trait in random.sample(self.personality_traits, random.randint(3, 6))
        }
        
        # 学習履歴
        completed_trainings = random.sample(
            self.training_modules, 
            random.randint(1, min(6, len(self.training_modules)))
        )
        
        # 現在の目標
        current_objectives = self._generate_objectives(department, skills)
        
        employee = Employee(
            id=employee_id,
            name=f"{first_name} {last_name}",
            email=f"{first_name.lower()}.{last_name.lower()}@company.com",
            department=department,
            hire_date=hire_date,
            skills=skills,
            learning_pace=round(learning_pace, 2),
            preferred_learning_style=random.choice(["visual", "hands-on", "reading", "discussion"]),
            performance_metrics=performance_metrics,
            overall_rating=random.uniform(2.5, 4.5),
            strengths=strengths,
            improvement_areas=improvement_areas,
            personality_traits=personality_traits,
            completed_trainings=completed_trainings,
            current_objectives=current_objectives
        )
        
        return employee
    
    def generate_employee_batch(self, count: int = 10, 
                               department_distribution: Dict[Department, int] = None) -> List[Employee]:
        """複数の社員データを生成"""
        
        if department_distribution is None:
            # デフォルトの分布
            department_distribution = {
                Department.ENGINEERING: count // 3,
                Department.SALES: count // 4,
                Department.MARKETING: count // 5,
                Department.HR: count // 8,
                Department.FINANCE: count // 8,
                Department.OPERATIONS: count - (count//3 + count//4 + count//5 + count//8 + count//8)
            }
        
        employees = []
        experience_levels = ["entry", "fast_learner", "struggling"]
        
        for department, dept_count in department_distribution.items():
            for _ in range(dept_count):
                experience_level = random.choice(experience_levels)
                employee = self.generate_employee(department, experience_level)
                employees.append(employee)
        
        return employees
    
    def generate_diverse_scenarios(self) -> List[Employee]:
        """多様なシナリオの社員データを生成"""
        scenarios = [
            # 高パフォーマンス新人
            {"department": Department.ENGINEERING, "experience_level": "fast_learner"},
            
            # 苦戦している新人
            {"department": Department.SALES, "experience_level": "struggling"},
            
            # 平均的な新人
            {"department": Department.MARKETING, "experience_level": "entry"},
            
            # 技術系の新人
            {"department": Department.ENGINEERING, "experience_level": "entry"},
            
            # コミュニケーション重視の部署
            {"department": Department.HR, "experience_level": "entry"},
            
            # 分析系の新人
            {"department": Department.FINANCE, "experience_level": "fast_learner"}
        ]
        
        employees = []
        for scenario in scenarios:
            employee = self.generate_employee(**scenario)
            employees.append(employee)
        
        return employees
    
    def _generate_skills(self, department: Department, experience_level: str) -> List[Skill]:
        """部署に適したスキルを生成"""
        department_skills = self.skill_names.get(department, ["Communication", "Problem Solving"])
        skill_count = random.randint(4, 8)
        selected_skills = random.sample(department_skills, min(skill_count, len(department_skills)))
        
        skills = []
        for skill_name in selected_skills:
            # 経験レベルに基づいてスキルレベルと進捗を調整
            if experience_level == "fast_learner":
                level = random.choice([SkillLevel.BEGINNER, SkillLevel.INTERMEDIATE])
                progress_rate = random.uniform(60, 95)
            elif experience_level == "struggling":
                level = SkillLevel.BEGINNER
                progress_rate = random.uniform(20, 50)
            else:  # entry
                level = SkillLevel.BEGINNER
                progress_rate = random.uniform(40, 70)
            
            skill = Skill(
                name=skill_name,
                level=level,
                last_assessed=datetime.now() - timedelta(days=random.randint(1, 30)),
                progress_rate=round(progress_rate, 1)
            )
            skills.append(skill)
        
        return skills
    
    def _generate_performance_metrics(self, department: Department) -> List[PerformanceMetric]:
        """部署に適したパフォーマンス指標を生成"""
        
        metric_templates = {
            Department.ENGINEERING: [
                ("Code Quality Score", 70, 85),
                ("Project Completion Rate", 80, 95),
                ("Bug Resolution Time", 60, 80),
                ("Code Review Participation", 75, 90)
            ],
            Department.SALES: [
                ("Sales Target Achievement", 70, 100),
                ("Customer Satisfaction", 80, 95),
                ("Lead Conversion Rate", 60, 85),
                ("Call Volume", 75, 90)
            ],
            Department.MARKETING: [
                ("Campaign ROI", 65, 85),
                ("Content Engagement Rate", 70, 90),
                ("Lead Generation", 75, 95),
                ("Brand Awareness Score", 60, 80)
            ],
            Department.HR: [
                ("Recruiting Success Rate", 70, 90),
                ("Employee Satisfaction", 80, 95),
                ("Training Completion Rate", 85, 98),
                ("Compliance Score", 90, 100)
            ],
            Department.FINANCE: [
                ("Report Accuracy", 85, 98),
                ("Deadline Adherence", 80, 95),
                ("Analysis Quality", 70, 90),
                ("Process Efficiency", 75, 88)
            ],
            Department.OPERATIONS: [
                ("Process Efficiency", 75, 90),
                ("Quality Score", 80, 95),
                ("Cost Optimization", 70, 85),
                ("On-time Delivery", 85, 98)
            ]
        }
        
        templates = metric_templates.get(department, [
            ("Overall Performance", 70, 90),
            ("Task Completion Rate", 75, 95),
            ("Quality Score", 80, 92)
        ])
        
        metrics = []
        for metric_name, min_target, max_target in templates:
            target_value = random.uniform(min_target, max_target)
            
            # 実際の値は目標の80-120%の範囲で生成
            actual_value = target_value * random.uniform(0.8, 1.2)
            
            metric = PerformanceMetric(
                metric_name=metric_name,
                value=round(actual_value, 2),
                target_value=round(target_value, 2),
                achieved_date=datetime.now() - timedelta(days=random.randint(1, 60)),
                category=department.value
            )
            metrics.append(metric)
        
        return metrics
    
    def _generate_objectives(self, department: Department, skills: List[Skill]) -> List[str]:
        """現在の目標を生成"""
        objectives = []
        
        # スキルベースの目標
        low_progress_skills = [s for s in skills if s.progress_rate < 60]
        for skill in low_progress_skills[:2]:
            objectives.append(f"Improve {skill.name} proficiency")
        
        # 部署特有の目標
        department_objectives = {
            Department.ENGINEERING: [
                "Complete technical certification",
                "Lead a small development project",
                "Contribute to code review process"
            ],
            Department.SALES: [
                "Achieve monthly sales quota",
                "Build customer relationship skills",
                "Master CRM system usage"
            ],
            Department.MARKETING: [
                "Launch first marketing campaign",
                "Increase social media engagement",
                "Learn advanced analytics tools"
            ],
            Department.HR: [
                "Complete recruiting certification",
                "Improve interview skills",
                "Understand employment law basics"
            ],
            Department.FINANCE: [
                "Master financial modeling",
                "Improve Excel proficiency",
                "Complete accounting certification"
            ],
            Department.OPERATIONS: [
                "Optimize a key process",
                "Improve quality metrics",
                "Learn project management tools"
            ]
        }
        
        dept_objectives = department_objectives.get(department, ["Improve overall performance"])
        objectives.extend(random.sample(dept_objectives, min(2, len(dept_objectives))))
        
        return objectives[:4]  # 最大4つの目標
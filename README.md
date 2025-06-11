# Mentor Agent - AI Support for New Employee Education

## Overview

Mentor Agent is an AI agent that plays the role of a senior employee educating new employees. It analyzes new employee performance data to identify strengths and areas for improvement, providing autonomous and personalized support to promote their growth.

## Key Features

- **Comprehensive Analysis**: Multi-dimensional analysis of skills, learning pace, and performance metrics
- **Personalized Feedback**: AI-generated feedback adapted to individual learning styles and capabilities
- **Autonomous Support**: Proactive identification of issues and automatic support provision
- **Growth Tracking**: Time-series progress monitoring with detailed growth records
- **Adaptive Communication**: Communication style adjustment based on employee's listening ability and learning pace
- **Learning Path Design**: Customized 90-day growth plans with specific milestones and objectives

## Special Consideration for New Employees

This agent is specifically designed for new employees who may have limited listening skills or learning capacity:

- **Graduated explanations** based on learning pace
- **Supportive tone** for slower learners with detailed step-by-step guidance
- **Direct approach** for fast learners with concise, action-oriented feedback
- **Regular check-ins** with frequency adjusted to individual needs
- **Concrete action items** with clear deadlines and priorities

## Project Structure

```
menter_agent/
├── src/
│   ├── agent/         # Core logic of mentor agent
│   ├── models/        # Data model definitions
│   ├── services/      # Business logic services
│   └── utils/         # Utility functions
├── data/
│   ├── employees/     # Employee data
│   └── feedbacks/     # Feedback data
├── tests/             # Test cases
├── config/            # Configuration files
└── requirements.txt   # Dependencies
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd menter_agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "from src.agent import MentorAgent; print('Installation successful!')"
   ```

## Quick Start Demo

### Running the Demo

The easiest way to see the Mentor Agent in action is to run the provided demonstration:

```bash
python example.py
```

This will:
1. Create a sample new employee (田中太郎)
2. Initialize the mentor agent
3. Perform comprehensive employee analysis
4. Generate personalized feedback
5. Create a 90-day growth plan
6. Track progress and provide autonomous support
7. Save all data to the `data/` directory

### Demo Output Example

```
🤖 メンターエージェント デモンストレーション
==================================================

👤 新人社員: 田中太郎
📅 入社日: 2025-03-14
🏢 部署: engineering
📈 学習ペース: 0.8

📊 社員分析結果:
------------------------------
総合評価: Satisfactory
成長軌道: Slow
スキル数: 3
平均進捗: 49.0%

💬 個別フィードバック:
------------------------------
タイプ: constructive
カテゴリ: technical
要約: Performance feedback for 田中太郎
インパクトスコア: 5.0/10

📋 アクションアイテム:
   1. Focus on improving Technical documentation
      期限: 2025-07-12
      優先度: high

🎯 成長計画 (90日間):
------------------------------
目標:
   - Python Programming: beginner → intermediate (優先度: medium)
   - Project Management: beginner → intermediate (優先度: high)

📈 進捗トラッキング:
------------------------------
総合成長スコア: 5.0/10
成長トレンド: steady

🤝 自律的サポート例:
------------------------------
Skill Gapサポート:
   - Identify specific skill gaps
   - Recommend targeted learning resources
```

## Advanced Usage

### Creating Custom Employees

```python
from datetime import datetime, timedelta
from src.agent import MentorAgent
from src.models import Employee, Skill, SkillLevel, Department

# Create custom employee
employee = Employee(
    id="emp_002",
    name="Your Employee Name",
    email="employee@example.com",
    department=Department.ENGINEERING,
    hire_date=datetime.now() - timedelta(days=60),
    learning_pace=1.2,  # Adjust based on learning speed
    preferred_learning_style="visual",  # visual, auditory, kinesthetic
    # ... add more attributes
)

# Initialize mentor agent
mentor = MentorAgent()
mentor.initialize()

# Save employee data
mentor.save_employee(employee)

# Generate analysis and feedback
analysis = mentor.analyze_employee(employee)
feedback = mentor.generate_feedback(employee)
growth_plan = mentor.create_growth_plan(employee)
```

### Providing Targeted Support

```python
# Provide specific support based on issues
support_response = mentor.provide_support(employee, "skill_gap")
print(f"Support provided: {support_response['support_provided']}")

# Available support types:
# - "skill_gap": For employees lacking specific skills
# - "motivation": For employees with low motivation
# - "communication": For communication-related issues
# - "workload": For workload management problems
```

### Data Management

```python
# Load existing employee
employee = mentor.load_employee("employee_id")

# Track progress over time
from datetime import datetime, timedelta
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()
growth_record = mentor.track_progress(employee, start_date, end_date)

print(f"Growth trend: {growth_record.growth_trend}")
print(f"Overall score: {growth_record.overall_growth_score}")
```

## Data Storage

The agent automatically saves data in JSON format:

- **Employee data**: `data/employees/{employee_id}.json`
- **Feedback records**: `data/feedbacks/{feedback_id}.json`

### Example Data Structure

**Employee Data** (`data/employees/emp_001.json`):
```json
{
  "id": "emp_001",
  "name": "田中太郎",
  "department": "engineering",
  "skills": [
    {
      "name": "Python Programming",
      "level": "beginner",
      "progress_rate": 45.0
    }
  ],
  "learning_pace": 0.8,
  "strengths": ["Quick learner", "Team player"],
  "improvement_areas": ["Technical documentation", "Time management"]
}
```

## Customization

### Adjusting Communication Style

The agent automatically adjusts its communication style based on:

- **Learning pace < 0.7**: Supportive, detailed explanations
- **Learning pace > 1.3**: Direct, concise feedback
- **Standard pace**: Balanced approach

### Custom Configuration

```python
config = {
    "feedback_frequency": "weekly",  # weekly, bi-weekly, monthly
    "min_skill_threshold": 40,       # Minimum skill level for focus
    "growth_plan_duration": 90       # Days for growth planning
}

mentor = MentorAgent(config=config)
```

## License

MIT License
# メンターエージェント - 新人社員教育支援AI

## 概要

メンターエージェントは、新人社員を教育する先輩社員の役割を担うAIエージェントです。新人社員のパフォーマンスデータを分析し、強みと改善点を特定して、自律的で個別化されたサポートを提供し、成長を促進します。

## 主要機能

- **🧠 LLM統合分析**: OpenAI APIを活用した自然言語による高度な分析とフィードバック
- **🔀 ハイブリッドシステム**: LLM + ルールベースによる確実で柔軟なサポート
- **📊 包括的分析**: スキル、学習ペース、パフォーマンス指標の多次元分析
- **💬 個別化フィードバック**: AI生成による自然で個人に最適化されたフィードバック
- **🤝 自律的サポート**: 問題の予防的特定と状況に応じた自動サポート提供
- **📈 成長トラッキング**: 詳細な成長記録による時系列進捗監視
- **🎯 適応的コミュニケーション**: 社員の理解力と学習ペースに基づくコミュニケーションスタイル調整
- **🗺️ 学習パス設計**: 具体的なマイルストーンと目標を含む90日間のカスタマイズ成長計画

## 新人社員への特別配慮

このエージェントは、聞く能力や学習能力に限りがある新人社員を特に考慮して設計されています：

- **段階的説明**: 学習ペースに基づいた説明レベルの調整
- **サポート的アプローチ**: 学習の遅い社員には詳細なステップバイステップ指導
- **直接的アプローチ**: 学習の早い社員には簡潔で行動指向のフィードバック
- **定期チェックイン**: 個人のニーズに応じた頻度調整
- **具体的アクション**: 明確な期限と優先度を持つ実行可能な項目

## プロジェクト構造

```
menter_agent/
├── src/
│   ├── agent/         # メンターエージェントのコアロジック
│   ├── models/        # データモデル定義（Employee, Feedback, GrowthRecord等）
│   ├── services/      # ビジネスロジックサービス（LLMService含む）
│   └── utils/         # ユーティリティ関数
├── data/
│   ├── employees/     # 社員データ
│   └── feedbacks/     # フィードバックデータ
├── tests/             # テストケース
├── config/            # 設定ファイル
├── example.py         # デモンストレーション用スクリプト
└── requirements.txt   # 依存関係
```

## インストール

### 前提条件

- Python 3.8以上
- Git（リポジトリのクローン用）

### セットアップ

1. **リポジトリのクローン**
   ```bash
   git clone <repository-url>
   cd menter_agent
   ```

2. **仮想環境の作成**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **依存関係のインストール**
   ```bash
   pip install -r requirements.txt
   ```

4. **インストールの確認**
   ```bash
   python -c "from src.agent import MentorAgent; print('インストール成功！')"
   ```

### LLM機能の設定

**🚀 LLM統合が完了しました！** エージェントはOpenAI APIを使用してより自然で個別化されたフィードバックを提供します。

#### OpenAI API設定

1. **.envファイルの作成**
   ```bash
   # プロジェクトルートに.envファイルを作成
   touch .env
   ```

2. **.envファイルの編集**
   ```bash
   # .env
   OPENAI_API_KEY=your-openai-api-key-here
   MODEL_NAME=gpt-3.5-turbo
   ```

3. **OpenAI APIキーの取得**
   - [OpenAI Platform](https://platform.openai.com/)でアカウント作成
   - API Keysセクションで新しいキーを生成
   - 上記の.envファイルに設定

#### フォールバック機能

**重要**: APIキーが設定されていない場合、システムは自動的にルールベースモードにフォールバックし、完全に動作します。LLM機能はオプションです。

## クイックスタート デモ

### デモの実行

メンターエージェントの動作を確認する最も簡単な方法は、提供されているデモンストレーションを実行することです：

```bash
python example.py
```

#### LLM統合デモの特徴

このコマンドで以下が実行されます：
1. 🤖 **LLMステータス確認**: OpenAI API接続状況とモードの表示
2. 👤 **サンプル新人社員（田中太郎）の作成**
3. 🔧 **メンターエージェントの初期化**（ハイブリッドモード）
4. 📊 **社員の包括的分析の実行**
5. 💬 **AI生成個別化フィードバック**（LLM + ルールベース）
6. 🎯 **90日間の成長計画作成**
7. 📈 **進捗トラッキングと自律的サポート提供**
8. 🔄 **LLMとルールベースの比較デモ**
9. 💾 **全データを`data/`ディレクトリに保存**

### デモ出力例（LLM統合版）

```
🤖 メンターエージェント デモンストレーション（LLM統合版）
============================================================

🔧 LLMステータス:
   - LLM利用可能: ✅
   - LLM有効: ✅
   - 動作モード: hybrid

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
要約: 技術文書作成と時間管理のスキル向上が必要です
詳細: 田中太郎さん、あなたの学習ペースは安定していますが、技術文書作成と
      時間管理が改善の余地があります...（LLM生成の自然な日本語）
インパクトスコア: 5.0/10

🤝 自律的サポート例（LLM強化）:
----------------------------------------

スキルギャップサポート:
   💬 AIメッセージ: 田中さん、学習ペースは問題ありません。あなたの強みを
                  活かしましょう！具体的なスキルを伸ばすために...
   📝 ソース: LLM生成

🔄 LLMとルールベースの比較:
----------------------------------------
ルールベース: 田中太郎さんへのフィードバック
LLM生成: 改善の余地あり。技術文書作成と時間管理に注力しましょう。
信頼度比較: ルール(0.85) vs LLM(0.95)

✅ LLM統合デモンストレーション完了!
🎯 LLM機能により、より自然で個別化されたフィードバックを提供しています
```

## 高度な使用方法

### カスタム社員の作成

```python
from datetime import datetime, timedelta
from src.agent import MentorAgent
from src.models import Employee, Skill, SkillLevel, Department

# カスタム社員の作成
employee = Employee(
    id="emp_002",
    name="山田花子",
    email="yamada@example.com",
    department=Department.ENGINEERING,
    hire_date=datetime.now() - timedelta(days=60),
    learning_pace=1.2,  # 学習速度に基づいて調整
    preferred_learning_style="visual",  # visual, auditory, kinesthetic
    # ... その他の属性を追加
)

# メンターエージェントの初期化
mentor = MentorAgent()
mentor.initialize()

# 社員データの保存
mentor.save_employee(employee)

# 分析とフィードバックの生成
analysis = mentor.analyze_employee(employee)
feedback = mentor.generate_feedback(employee)
growth_plan = mentor.create_growth_plan(employee)
```

### 対象的サポートの提供

```python
# 問題に基づく特定サポートの提供
support_response = mentor.provide_support(employee, "skill_gap")
print(f"提供されたサポート: {support_response['support_provided']}")

# 利用可能なサポートタイプ:
# - "skill_gap": 特定スキル不足の社員向け
# - "motivation": モチベーションが低い社員向け
# - "communication": コミュニケーション関連の問題
# - "workload": 作業負荷管理の問題
```

### データ管理

```python
# 既存社員の読み込み
employee = mentor.load_employee("employee_id")

# 時系列での進捗トラッキング
from datetime import datetime, timedelta
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()
growth_record = mentor.track_progress(employee, start_date, end_date)

print(f"成長トレンド: {growth_record.growth_trend}")
print(f"総合スコア: {growth_record.overall_growth_score}")
```

## データストレージ

エージェントは自動的にデータをJSON形式で保存します：

- **社員データ**: `data/employees/{employee_id}.json`
- **フィードバック記録**: `data/feedbacks/{feedback_id}.json`

### データ構造例

**社員データ** (`data/employees/emp_001.json`):
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
  "strengths": ["素早い学習者", "チームプレイヤー"],
  "improvement_areas": ["技術文書作成", "時間管理"]
}
```

**フィードバックデータ** (`data/feedbacks/{feedback_id}.json`):
```json
{
  "id": "fb_001_20250612",
  "employee_id": "emp_001",
  "type": "constructive",
  "summary": "田中太郎さんのパフォーマンスフィードバック",
  "detailed_feedback": "分析に基づき、あなたの総合パフォーマンスは良好です...",
  "action_items": [
    {
      "description": "技術文書作成スキルの向上",
      "due_date": "2025-07-12",
      "priority": "high"
    }
  ]
}
```

## カスタマイズ

### コミュニケーションスタイルの調整

エージェントは以下に基づいて自動的にコミュニケーションスタイルを調整します：

- **学習ペース < 0.7**: サポート的、詳細な説明
- **学習ペース > 1.3**: 直接的、簡潔なフィードバック
- **標準ペース**: バランスの取れたアプローチ

### カスタム設定（LLM統合対応）

```python
config = {
    "use_llm": True,                    # LLM機能の有効/無効
    "feedback_frequency": "weekly",     # weekly, bi-weekly, monthly
    "min_skill_threshold": 40,          # フォーカスする最小スキルレベル
    "growth_plan_duration": 90,         # 成長計画の日数
    "support_threshold": 0.7            # サポート介入の閾値
}

mentor = MentorAgent(config=config)

# LLMモードの動的切り替え
mentor.toggle_llm_mode(False)  # ルールベースモードに切り替え
mentor.toggle_llm_mode(True)   # LLMモードに切り替え

# LLMステータスの確認
status = mentor.get_llm_status()
print(f"動作モード: {status['mode']}")  # hybrid, rule-based
```

### フィードバックスタイルのカスタマイズ

```python
from src.services import FeedbackService

feedback_service = FeedbackService()

# 学習ペースに応じたメッセージ調整
adjusted_message = feedback_service.adjust_communication_style(
    employee, 
    "あなたのプログラミングスキルを向上させる必要があります"
)

# 励ましのメッセージ生成
encouragement = feedback_service.generate_encouragement(employee)
print(f"励まし: {encouragement}")
```

## トラブルシューティング

### よくある問題

1. **ImportError**: Pythonパスの確認
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Pydantic compatibility error**: Pydantic v1/v2の両方をサポート済み
   - 自動的にバージョンを検出し適切なメソッドを使用

3. **JSON serialization error**: datetimeオブジェクトの処理は自動化済み

4. **データファイルが見つからない**: `data/`ディレクトリは自動作成されます

### ログの確認

```python
import logging
logging.basicConfig(level=logging.INFO)

mentor = MentorAgent()
# ログ出力でデバッグ情報を確認
```

## 貢献とサポート

### 開発者向け

プロジェクトへの貢献を歓迎します：

1. リポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

### 今後の拡張予定

- ✅ **LLM統合**: OpenAI APIを使用した自然言語によるフィードバック生成 **（完了）**
- 🔄 **高度なプロンプト**: 業界特化型やスキル別の専門プロンプト
- 🌐 **Web UI**: ブラウザベースのインターフェース
- 📊 **レポート生成**: PDF/Excel形式での進捗レポート
- 👥 **チーム分析**: 部署やチーム全体の分析機能
- 🌍 **多言語サポート**: 英語・中国語などの対応
- ⚡ **リアルタイム分析**: 継続的なパフォーマンス監視
- 🧠 **他のLLMサポート**: Claude、Gemini等の追加サポート

### 現在の実装状況

**✅ 完了済み**: 
- ハイブリッドシステム（LLM + ルールベース）
- OpenAI API統合
- 自動フォールバック機能
- 日本語対応

**🔄 進行中**: 
- より高度なプロンプト設計
- パフォーマンス最適化

**📋 今後の計画**: 
- Web UI開発
- マルチLLMサポート

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # アプリケーション設定
    app_name: str = "メンターエージェント"
    version: str = "1.0.0"
    debug: bool = False
    
    # API設定
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # データベース設定
    database_url: str = "sqlite:///./data/mentor.db"
    
    # LLM設定
    openai_api_key: Optional[str] = None
    model_name: str = "gpt-3.5-turbo"
    
    # フィードバック設定
    feedback_max_length: int = 1000
    feedback_min_length: int = 100
    
    # 成長トラッキング設定
    evaluation_period_days: int = 30
    min_data_points: int = 5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
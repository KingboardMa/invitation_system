import os
from typing import List

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    # 数据库配置
    database_url: str = "sqlite:///./invitation_codes.db"

    # API配置
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    # CORS配置
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]

    # 安全配置
    max_requests_per_ip_per_hour: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

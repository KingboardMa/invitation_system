import os
from typing import List

import os
from typing import List

class Settings:
    """应用配置设置"""
    
    def __init__(self):
        # 数据库配置
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./invitation_codes.db")
        
        # API配置
        self.api_v1_prefix = os.getenv("API_V1_PREFIX", "/api/v1")
        self.debug = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
        
        # CORS配置
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080,http://127.0.0.1:8080,http://code.movoui.cn,https://code.movoui.cn")
        self.cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]
        
        # 安全配置
        self.max_requests_per_ip_per_hour = int(os.getenv("MAX_REQUESTS_PER_IP_PER_HOUR", "10"))

settings = Settings()

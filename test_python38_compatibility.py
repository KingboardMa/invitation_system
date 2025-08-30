#!/usr/bin/env python3
"""
测试Python 3.8兼容性脚本
"""

import sys
import os
from pathlib import Path

print(f"Python版本: {sys.version}")

# 添加backend目录到路径
sys.path.insert(0, str(Path(__file__).parent / "backend"))

try:
    # 测试导入所有主要模块
    print("测试导入模块...")

    from cli.import_codes import read_codes_from_file
    print("✅ cli.import_codes 导入成功")

    from config.settings import Settings
    settings = Settings()
    print("✅ config.settings 导入成功")

    from schemas import OfferInfo, ClaimRequest, StatsData
    print("✅ schemas 导入成功")

    from services.code_service import CodeService
    print("✅ services.code_service 导入成功")

    from models.database import create_tables
    print("✅ models.database 导入成功")

    print("\n🎉 所有模块导入成功，Python 3.8兼容性问题已修复！")

except Exception as e:
    print(f"\n❌ 导入失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

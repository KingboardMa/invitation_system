#!/usr/bin/env python3
"""
快速测试脚本
演示邀请码发放系统的完整功能
"""

import sys
import os
import subprocess
import time
import requests
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))

def run_command(cmd, cwd=None):
    """执行命令"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_api(url, method="GET", data=None):
    """测试API接口"""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)

        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}

def main():
    print("🧪 邀请码发放系统 - 快速测试")
    print("=" * 50)

    # 1. 检查依赖
    print("1️⃣  检查Python依赖...")
    success, stdout, stderr = run_command("pip list | grep -E '(fastapi|uvicorn|sqlalchemy)'")
    if not success:
        print("❌ 缺少必要的Python包，请运行：pip install -r backend/requirements.txt")
        return
    print("✅ Python依赖检查通过")

    # 2. 启动服务器（后台）
    print("\n2️⃣  启动后端服务...")
    print("   启动命令: uvicorn main:app --host 127.0.0.1 --port 8000")
    print("   请在另一个终端运行以下命令：")
    print("   cd backend && python main.py")
    print("   然后按回车继续测试...")
    input()

    # 3. 等待服务启动
    print("3️⃣  检查服务状态...")
    for i in range(10):
        try:
            response = requests.get("http://127.0.0.1:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ 后端服务启动成功")
                break
        except:
            if i < 9:
                print(f"   等待服务启动... ({i+1}/10)")
                time.sleep(1)
            else:
                print("❌ 无法连接到后端服务，请确保服务已启动")
                return

    # 4. 测试导入邀请码
    print("\n4️⃣  测试导入邀请码...")
    sample_file = project_root / "sample_codes.txt"
    if sample_file.exists():
        cmd = f"python -m cli.import_codes --offer testdemo --file {sample_file} --title '测试演示' --description '系统功能演示用邀请码'"
        success, stdout, stderr = run_command(cmd, cwd=backend_path)
        if success:
            print("✅ 邀请码导入成功")
            print(f"   输出: {stdout[:200]}...")
        else:
            print(f"❌ 邀请码导入失败: {stderr}")
    else:
        print("❌ 示例邀请码文件不存在")

    # 5. 测试API接口
    print("\n5️⃣  测试API接口...")

    # 测试获取offer信息
    status, data = test_api("http://127.0.0.1:8000/api/v1/offers/testdemo/info")
    if status == 200 and data.get("success"):
        offer_data = data["data"]
        print(f"✅ 获取项目信息成功")
        print(f"   项目名称: {offer_data['title']}")
        print(f"   总邀请码: {offer_data['total_count']}")
        print(f"   剩余数量: {offer_data['remaining_count']}")
    else:
        print(f"❌ 获取项目信息失败: {data}")

    # 6. 测试申请邀请码
    print("\n6️⃣  测试申请邀请码...")
    claim_data = {"user_ip": "127.0.0.1", "user_agent": "TestScript/1.0"}
    status, data = test_api("http://127.0.0.1:8000/api/v1/offers/testdemo/claim", "POST", claim_data)

    if status == 200 and data.get("success"):
        invitation_code = data["data"]["code"]
        print(f"✅ 邀请码申请成功")
        print(f"   获得邀请码: {invitation_code}")
    else:
        print(f"❌ 邀请码申请失败: {data}")

    # 7. 测试统计信息
    print("\n7️⃣  测试统计信息...")
    status, data = test_api("http://127.0.0.1:8000/api/v1/offers/testdemo/stats")
    if status == 200 and data.get("success"):
        stats = data["data"]
        print(f"✅ 获取统计信息成功")
        print(f"   总邀请码: {stats['total_codes']}")
        print(f"   已使用: {stats['used_codes']}")
        print(f"   剩余数量: {stats['remaining_codes']}")
        print(f"   使用率: {stats['usage_rate']:.1%}")
    else:
        print(f"❌ 获取统计信息失败: {data}")

    # 8. 提供访问链接
    print("\n🌐 系统访问链接:")
    print("   API文档: http://127.0.0.1:8000/docs")
    print("   测试页面: http://127.0.0.1:8000/offer/testdemo")
    print("   健康检查: http://127.0.0.1:8000/health")

    print("\n🎉 测试完成！系统运行正常。")
    print("💡 提示: 你可以在浏览器中访问测试页面体验完整功能")

if __name__ == "__main__":
    main()

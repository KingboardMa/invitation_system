#!/bin/bash

echo "🚀 启动邀请码发放系统"
echo "========================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python 3.8+"
    exit 1
fi

# 进入后端目录
cd backend || exit 1

# 检查并安装依赖
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt 文件不存在"
    exit 1
fi

echo "📦 检查依赖包..."
pip install -r requirements.txt

# 启动服务
echo "🚀 启动后端服务..."
echo "📖 API文档: http://localhost:8000/docs"
echo "🌐 示例页面: http://localhost:8000/offer/fellou"
echo "💡 按Ctrl+C停止服务"
echo "========================"

python main.py

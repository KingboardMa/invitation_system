# 邀请码发放系统

一个功能完整的前后端分离邀请码发放系统，支持多项目管理和统计。

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动后端服务

```bash
cd backend
python main.py
```

服务将在 `http://localhost:8000` 启动。

### 3. 访问系统

- **API文档**: http://localhost:8000/docs
- **邀请码页面**: http://localhost:8000/offer/{offer_name}
- **健康检查**: http://localhost:8000/health

## 📋 功能特性

### 核心功能
- ✅ 多项目邀请码管理
- ✅ 实时统计信息显示
- ✅ 一键领取和复制邀请码
- ✅ 防重复申请机制
- ✅ 用户行为记录和审计

### 管理功能
- ✅ 命令行批量导入邀请码
- ✅ 项目统计信息查询
- ✅ 使用记录追踪

## 🛠 使用方法

### 1. 导入邀请码

首先准备一个包含邀请码的文本文件，每行一个邀请码：

```txt
ABC123DEF456
XYZ789GHI012
...
```

使用命令行工具导入：

```bash
cd backend
python -m cli.import_codes --offer fellou --file codes.txt --title "Fellou邀请码" --description "Fellou产品专属邀请码"
```

参数说明：
- `--offer`: 项目名称（必需）
- `--file`: 邀请码文件路径（必需）
- `--title`: 项目显示标题（可选，新建项目时使用）
- `--description`: 项目描述（可选，新建项目时使用）

### 2. 用户领取邀请码

用户访问：`http://localhost:8000/offer/fellou`

页面功能：
- 显示项目信息和剩余数量
- 点击按钮领取邀请码
- 一键复制到剪贴板

### 3. 查看统计信息

访问管理接口查看详细统计：
```
GET /api/v1/offers/{offer_name}/stats
```

## 📁 项目结构

```
invitation_system/
├── backend/                    # 后端代码
│   ├── main.py                # FastAPI应用入口
│   ├── requirements.txt       # Python依赖
│   ├── .env                  # 环境配置
│   ├── config/               # 配置文件
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── models/               # 数据模型
│   │   ├── __init__.py
│   │   ├── database.py       # 数据库配置
│   │   ├── offer.py          # Offer模型
│   │   └── invitation_code.py # 邀请码模型
│   ├── services/             # 业务逻辑
│   │   ├── __init__.py
│   │   ├── offer_service.py  # Offer服务
│   │   └── code_service.py   # 邀请码服务
│   ├── routers/              # API路由
│   │   ├── __init__.py
│   │   └── offers.py         # Offer相关API
│   ├── cli/                  # 命令行工具
│   │   ├── __init__.py
│   │   └── import_codes.py   # 导入工具
│   └── schemas.py            # 数据传输对象
├── frontend/                 # 前端代码
│   └── index.html           # 单页应用
└── README.md                # 项目说明
```

## 🔧 API接口

### 获取项目信息
```http
GET /api/v1/offers/{offer_name}/info
```

响应：
```json
{
    "success": true,
    "data": {
        "name": "fellou",
        "title": "Fellou邀请码",
        "description": "Fellou产品邀请码发放",
        "total_count": 1000,
        "remaining_count": 856,
        "is_active": true
    }
}
```

### 申请邀请码
```http
POST /api/v1/offers/{offer_name}/claim
Content-Type: application/json

{
    "user_ip": "可选",
    "user_agent": "可选"
}
```

成功响应：
```json
{
    "success": true,
    "data": {
        "code": "ABC123DEF456",
        "message": "邀请码获取成功"
    }
}
```

### 获取统计信息
```http
GET /api/v1/offers/{offer_name}/stats
```

## ⚙️ 配置说明

### 环境变量 (.env)

```bash
# 数据库配置
DATABASE_URL=sqlite:///./invitation_codes.db

# API配置
DEBUG=true
API_V1_PREFIX=/api/v1

# CORS配置
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# 安全配置
MAX_REQUESTS_PER_IP_PER_HOUR=10
```

## 🗄️ 数据库

系统使用SQLite数据库，包含两个主要表：

- **offers**: 存储项目信息
- **invitation_codes**: 存储邀请码和使用记录

数据库文件默认存储在 `backend/invitation_codes.db`

## 🚀 部署

### 开发环境

```bash
# 后端
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 前端已集成在后端中，无需单独部署
```

### 生产环境

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --host 0.0.0.0 --port 8000
```

建议使用以下工具进行生产部署：
- **进程管理**: PM2, Supervisor, systemd
- **反向代理**: Nginx
- **HTTPS**: Let's Encrypt

## 🔒 安全特性

- IP地址记录和限制
- 用户代理追踪
- 邀请码使用不可逆转
- 完整的操作日志记录
- CORS跨域保护

## 📊 监控和日志

系统自动记录：
- 邀请码申请记录
- API访问日志
- 错误和异常信息
- 性能指标

## 🛣️ 未来规划

- [ ] 管理员Web界面
- [ ] 用户认证系统
- [ ] 邀请码有效期管理
- [ ] 使用统计分析
- [ ] 多种邀请码格式支持
- [ ] Redis缓存支持
- [ ] 多数据库支持

## 📝 示例场景

### 场景1: 创建新项目并导入邀请码

```bash
# 1. 准备邀请码文件 codes.txt
echo "CODE001\nCODE002\nCODE003" > codes.txt

# 2. 导入邀请码
python -m cli.import_codes --offer testproject --file codes.txt --title "测试项目" --description "这是一个测试项目"

# 3. 用户访问页面
# http://localhost:8000/offer/testproject
```

### 场景2: 查看项目统计

```bash
# 访问统计API
curl http://localhost:8000/api/v1/offers/testproject/stats
```

## ❓ 常见问题

**Q: 如何修改数据库配置？**
A: 修改 `.env` 文件中的 `DATABASE_URL` 变量。

**Q: 如何添加新的项目？**
A: 使用 `import_codes.py` 命令行工具，如果项目不存在会自动创建。

**Q: 如何限制用户申请次数？**
A: 系统会记录IP地址，可以在代码中添加限流逻辑。

**Q: 如何备份数据？**
A: 复制 `invitation_codes.db` 文件即可备份所有数据。

## 📄 许可证

MIT License

---

**开发者**: Assistant
**版本**: 1.0.0
**更新时间**: 2025-08-30

# Medical Triage Agent

## 项目简介

Medical Triage Agent 是一个面向常见症状咨询场景的医疗问诊智能体系统，通过安全门控、追问补全、医学知识库检索、风险分级和建议生成，为用户提供非诊断性质的就医建议与风险提示。

## 方向

方向一：Agentic AI 原生开发。

本项目从零构建一个垂直领域 AI Agent 系统，重点展示 SDD 规格驱动开发、工具/函数化模块调用、RAG 检索增强、对话记忆、多步骤推理、可观测日志和行为评估。

## 技术栈

- AI IDE: Trae CN / Codex 辅助开发
- LLM: 阿里云 DashScope 兼容 OpenAI 接口的 Qwen 模型
- Agent 编排: Python 多 Agent 协作编排，核心入口为 `src/app/agents/orchestrator.py`
- RAG: LangChain + Chroma + DashScope Embeddings
- Backend: FastAPI + SQLAlchemy + SQLite
- Frontend: React + TypeScript + Vite + Tailwind CSS
- 测试: Pytest
- 基础设施: Git / GitHub，环境变量管理，运行时日志

## 目录结构

```plain
.
├── src/
│   ├── app/                 # Python 后端源码
│   │   ├── agents/          # Agent 模块：安全门、追问、RAG、风险分类、建议生成、摘要
│   │   ├── api/             # FastAPI 路由：chat、triage、summary、feedback
│   │   ├── database/        # SQLAlchemy 模型与 CRUD
│   │   ├── rag/medical_docs/# 医学知识库 Markdown 文档
│   │   ├── schemas/         # Pydantic 请求/响应模型
│   │   └── utils/           # 配置、日志、LLM 客户端
│   ├── services/            # React 前端 API 封装
│   ├── App.tsx              # React 主界面
│   └── main.tsx             # React 入口
├── tests/                   # Agent 行为与风险规则测试
├── docs/                    # CS599 报告、规格与架构文档
│   ├── CS599_大作业报告.pdf  # 最终提交报告
│   ├── CS599_大作业报告.md   # 报告源文件
│   ├── architecture.md      # 架构说明
│   └── specs.md             # SDD 规格文档
├── index.html               # Vite 前端入口 HTML
├── pyproject.toml           # Python 项目配置与 pytest 配置
├── requirements.txt         # Python 依赖
├── package.json             # 前端依赖与脚本
├── package-lock.json        # 前端锁文件
├── uv.lock                  # Python 依赖锁文件
└── .env.example             # 环境变量示例
```

## 环境搭建

### 1. 安装后端依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest
```

也可以使用 `uv`：

```bash
uv sync --group dev
```

### 2. 配置环境变量

复制示例文件并填写自己的 API Key。不要把真实 Key 提交到 GitHub。

```bash
cp .env.example .env
```

`.env` 示例：

```plain
DASHSCOPE_API_KEY=your_dashscope_api_key_here
DASHSCOPE_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LOG_LEVEL=INFO
```

### 3. 启动后端

```bash
source .venv/bin/activate
PYTHONPATH=src uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端接口文档地址：

```plain
http://localhost:8000/docs
```

### 4. 启动前端

```bash
npm install
npm run dev
```

前端默认地址：

```plain
http://localhost:5173
```

### 5. 运行测试

```bash
source .venv/bin/activate
pytest
```

## 核心能力

- 安全门控：优先识别胸痛、呼吸困难、意识模糊等红旗症状，并直接输出急救建议。
- 多轮追问：对症状、部位、持续时间、严重程度、伴随症状进行信息完整性检查。
- Agentic RAG：从本地医学知识库检索相关片段，作为建议生成上下文。
- 风险分级：根据症状、年龄、病史、特殊人群和体温输出 A/B/C/D 风险等级。
- 对话记忆：SQLite 保存用户会话、问诊消息、风险结果和反馈。
- 可观测性：日志记录关键链路，包括红旗症状、追问字段和最终风险等级。

## API 摘要

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/chat/` | POST | 多轮问诊主入口 |
| `/chat/history/{session_id}` | GET | 获取历史消息 |
| `/triage/risk` | POST | 独立风险评估 |
| `/triage/red-flags` | POST | 红旗症状检测 |
| `/summary/{consultation_id}` | GET | 生成问诊摘要 |
| `/feedback/` | POST | 提交用户反馈 |

## 项目状态

- [x] Proposal
- [x] MVP
- [x] Final

## 课程交付说明

- 报告源文件：`docs/CS599_大作业报告.md`
- PDF 报告：`docs/CS599_大作业报告.pdf`
- 架构说明：`docs/architecture.md`
- Specs 文档：`docs/specs.md`

提交前请确认 GitHub 仓库名称为 `cs599-project`，如果仓库为 Private，请添加 `qxr777` 为 Collaborator。

## 不提交的本地文件

以下文件或目录属于本地运行产物，已通过 `.gitignore` 排除：

- `.env`
- `.venv/`
- `node_modules/`
- `dist/`
- `data/`
- `logs/`
- `.pytest_cache/`
- `__pycache__/`

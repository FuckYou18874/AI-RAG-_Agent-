# 🤖 智扫通机器人智能客服系统

基于 RAG 和 LangGraph 的扫地机器人智能客服 Agent 系统。

## ✨ 功能特性

- **ReAct Agent**: 基于 LangGraph 的智能体实现，支持自主思考与工具调用
- **RAG 知识库**: 使用 ChromaDB + 通义千问 Embedding 实现知识检索
- **多轮对话**: 支持会话记忆管理，实现上下文连贯的多轮对话
- **工具调用**: 天气查询、用户报告生成、知识检索等多种工具
- **流式响应**: 支持 SSE 流式输出，实时显示回复

## 🛠️ 技术栈

### 后端
- Python 3.10+
- FastAPI
- LangGraph / LangChain
- ChromaDB
- 通义千问大模型

### 前端
- Vue 3
- Vite
- Axios

## 📦 安装

```bash
# 克隆项目
git clone https://github.com/FuckYou18874/AI-RAG-_Agent-.git

# 安装后端依赖
cd AI-RAG-_Agent-
python -m venv venv
venv\Scripts\activate  # Windows
pip install fastapi uvicorn pydantic langchain langchain-chroma langchain-community dashscope

# 安装前端依赖
cd frontend
npm install
```

## 🚀 启动

```bash
# 启动后端 (端口 8001)
python -m uvicorn api.fastapi_server:app --host 0.0.0.0 --port 8001

# 启动前端 (端口 3000)
cd frontend
npm run dev
```

## 📖 API 文档

启动后端后访问: http://localhost:8001/docs

## 📝 配置

在 `config/` 目录下配置:
- `agent.yml`: Agent 配置
- `chroma.yml`: 向量库配置
- `prompts.yml`: 提示词配置

## 📄 License

MIT License
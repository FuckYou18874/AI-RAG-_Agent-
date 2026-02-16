import uuid
from typing import AsyncGenerator, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent.react_agent import ReactAgent
from utils.memory_manager import session_manager
from utils.logger_handler import logger
import json

app = FastAPI(
    title="智扫通机器人智能客服API",
    description="基于LangChain Agent的智能客服系统",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agents_cache = {}


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    status: str


class SessionInfo(BaseModel):
    session_id: str
    message_count: int


def get_or_create_agent(session_id: str) -> ReactAgent:
    if session_id not in agents_cache:
        agents_cache[session_id] = ReactAgent(session_id=session_id)
    return agents_cache[session_id]


@app.get("/")
async def root():
    return {"message": "智扫通机器人智能客服API", "version": "2.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "robot-api"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="消息不能为空")

        session_id = request.session_id or str(uuid.uuid4())
        agent = get_or_create_agent(session_id)

        response_chunks = []
        for chunk in agent.execute_stream(request.message):
            response_chunks.append(chunk)

        full_response = "".join(response_chunks)

        return ChatResponse(
            response=full_response,
            session_id=session_id,
            status="success"
        )

    except Exception as e:
        logger.error(f"[API]聊天接口错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="消息不能为空")

        session_id = request.session_id or str(uuid.uuid4())
        agent = get_or_create_agent(session_id)

        async def generate() -> AsyncGenerator[str, None]:
            yield f"data: {json.dumps({'type': 'session', 'session_id': session_id}, ensure_ascii=False)}\n\n"

            for chunk in agent.execute_stream(request.message):
                yield f"data: {json.dumps({'type': 'content', 'content': chunk}, ensure_ascii=False)}\n\n"

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    except Exception as e:
        logger.error(f"[API]流式聊天接口错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/session/new")
async def new_session():
    session_id = str(uuid.uuid4())
    return {"session_id": session_id, "status": "created"}


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    try:
        if session_id in agents_cache:
            del agents_cache[session_id]

        session_manager.delete_session(session_id)

        return {"session_id": session_id, "status": "cleared"}
    except Exception as e:
        logger.error(f"[API]清除会话错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/session/{session_id}/info")
async def get_session_info(session_id: str):
    try:
        session = session_manager.get_session(session_id)
        messages = session.messages
        return SessionInfo(
            session_id=session_id,
            message_count=len(messages)
        )
    except Exception as e:
        logger.error(f"[API]获取会话信息错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions")
async def list_sessions():
    sessions = session_manager.list_sessions()
    return {"sessions": sessions, "count": len(sessions)}


if __name__ == "__main__":
    import uvicorn
    print("🤖 机器人API服务启动中...")
    print("访问地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("聊天接口: POST http://localhost:8000/chat")
    print("流式聊天: POST http://localhost:8000/chat/stream")
    print("健康检查: GET http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)
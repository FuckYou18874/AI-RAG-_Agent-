@echo off
chcp 65001 >nul
echo ========================================
echo    智扫通机器人智能客服 - 启动脚本
echo ========================================
echo.

echo [1/2] 启动后端服务 (FastAPI)...
start "FastAPI Server" cmd /k "cd /d %~dp0 && .\venv\Scripts\python -m uvicorn api.fastapi_server:app --host 0.0.0.0 --port 8001"

timeout /t 3 /nobreak >nul

echo [2/2] 启动前端服务 (Vue)...
start "Vue Dev Server" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo 服务启动完成！
echo.
echo 后端API地址: http://localhost:8001
echo API文档地址: http://localhost:8001/docs
echo 前端访问地址: http://localhost:3000
echo ========================================
echo.
pause

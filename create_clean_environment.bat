@echo off
echo 创建全新的干净环境...
echo ================================

echo 1. 创建新的conda环境...
conda create -n ai_agent_clean python=3.9 -y

echo 2. 激活新环境...
conda activate ai_agent_clean

echo 3. 安装项目依赖...
pip install python-dotenv==1.0.0
pip install langchain==0.1.0 langchain-core==0.1.0 langchain-community==0.0.12
pip install chromadb==0.4.0 langchain-chroma==0.1.0
pip install dashscope==1.14.0
pip install pyyaml==6.0 requests==2.31.0

echo 4. 验证安装...
python -c "import langchain, chromadb, dashscope; print('环境配置完成！')"

echo 5. 复制项目文件到新环境...
xcopy "C:\Users\admin\Desktop\AI大模型RAG与智能体开发_Agent项目" "C:\Users\admin\Desktop\AI大模型RAG与智能体开发_Agent项目_clean" /E /I /H

echo 环境创建完成！
echo 请运行以下命令切换到新环境：
echo conda activate ai_agent_clean
echo cd C:\Users\admin\Desktop\AI大模型RAG与智能体开发_Agent项目_clean
pause
"""
详细调试脚本 - 定位NoneType错误的具体位置
"""
import traceback
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.logger_handler import logger
from agent.react_agent import ReactAgent

def debug_none_type_error():
    """调试NoneType错误"""
    print("🔬 开始详细调试...")
    print("=" * 50)
    
    try:
        print("1. 创建Agent实例...")
        agent = ReactAgent(session_id="debug_session")
        print("✅ Agent创建成功")
        print(f"   - 会话ID: {agent.session_id}")
        print(f"   - 记忆管理器类型: {type(agent.memory)}")
        print(f"   - Agent类型: {type(agent.agent)}")
        
        print("\n2. 测试简单查询...")
        test_query = "你好"
        
        print("3. 执行流式响应...")
        response_chunks = []
        for chunk in agent.execute_stream(test_query):
            response_chunks.append(chunk)
            print(f"   响应片段: {chunk.strip()}")
            
        print(f"\n✅ 执行完成，共收到 {len(response_chunks)} 个响应片段")
        
    except Exception as e:
        print(f"\n❌ 执行过程中出现错误:")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")
        print(f"   详细堆栈:")
        traceback.print_exc()
        
        # 更详细的错误分析
        print("\n🔍 错误位置分析:")
        tb = traceback.extract_tb(e.__traceback__)
        for frame in tb[-3:]:  # 显示最后3个堆栈帧
            print(f"   文件: {frame.filename}")
            print(f"   行号: {frame.lineno}")
            print(f"   函数: {frame.name}")
            print(f"   代码: {frame.line}")
            print()

def test_component_isolation():
    """隔离测试各个组件"""
    print("\n🧪 组件隔离测试...")
    print("=" * 30)
    
    # 测试1: 记忆管理器
    print("1. 测试记忆管理器...")
    try:
        from utils.memory_manager import session_manager
        session = session_manager.get_session("test_isolation")
        print("✅ 记忆管理器工作正常")
    except Exception as e:
        print(f"❌ 记忆管理器错误: {str(e)}")
    
    # 测试2: 模型工厂
    print("2. 测试模型工厂...")
    try:
        from model.factory import chat_model, embed_model
        print(f"✅ 聊天模型: {type(chat_model)}")
        print(f"✅ 嵌入模型: {type(embed_model)}")
    except Exception as e:
        print(f"❌ 模型工厂错误: {str(e)}")
    
    # 测试3: 工具函数
    print("3. 测试工具函数...")
    try:
        from agent.tools.agent_tools import get_weather, get_user_id
        print("✅ 工具函数导入成功")
    except Exception as e:
        print(f"❌ 工具函数错误: {str(e)}")

if __name__ == '__main__':
    debug_none_type_error()
    test_component_isolation()
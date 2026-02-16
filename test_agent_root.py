"""
在项目根目录运行的测试脚本
测试Agent功能和调试NoneType错误
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.react_agent import ReactAgent
from utils.logger_handler import logger

def test_agent_functionality():
    """测试Agent功能"""
    print("🤖 开始测试Agent功能...")
    print("=" * 40)
    
    try:
        # 创建Agent实例
        print("1. 创建Agent实例...")
        agent = ReactAgent(session_id="root_test_session")
        print("✅ Agent创建成功")
        
        # 测试简单对话
        print("\n2. 测试简单对话...")
        test_queries = [
            "你好",
            "介绍一下扫地机器人的选购要点"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- 测试 {i}: {query} ---")
            response_count = 0
            for chunk in agent.execute_stream(query):
                response_count += 1
                print(f"响应 {response_count}: {chunk.strip()}")
                if response_count >= 3:  # 限制输出长度
                    break
        
        print("\n🎉 Agent功能测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误:")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")
        import traceback
        traceback.print_exc()

def check_environment():
    """检查环境配置"""
    print("🔍 环境配置检查...")
    print("=" * 30)
    
    # 检查关键组件
    checks = [
        ("配置处理器", "utils.config_handler", ["rag_conf", "agent_conf"]),
        ("模型工厂", "model.factory", ["chat_model", "embed_model"]),
        ("记忆管理器", "utils.memory_manager", ["session_manager"]),
        ("提示词加载器", "utils.prompt_loader", ["load_system_prompts"]),
    ]
    
    for name, module_path, attributes in checks:
        try:
            module = __import__(module_path, fromlist=attributes)
            print(f"✅ {name}: 导入成功")
            for attr in attributes:
                if hasattr(module, attr):
                    value = getattr(module, attr)
                    if isinstance(value, dict):
                        print(f"   - {attr}: {len(value)} 个配置项")
                    else:
                        print(f"   - {attr}: {type(value).__name__}")
        except Exception as e:
            print(f"❌ {name}: {str(e)}")

if __name__ == '__main__':
    check_environment()
    print()
    test_agent_functionality()
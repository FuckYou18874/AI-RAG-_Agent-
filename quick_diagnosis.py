"""
快速验证和诊断脚本
检查当前环境状态并提供修复建议
"""
import sys
import os
import subprocess

def check_current_environment():
    """检查当前环境状态"""
    print("🔍 当前环境状态检查...")
    print("=" * 40)
    
    # 检查Python路径
    print(f"🐍 Python路径: {sys.executable}")
    print(f"📁 工作目录: {os.getcwd()}")
    
    # 检查关键包版本
    packages_to_check = ['langchain', 'langchain_core', 'langchain_community', 'chromadb', 'dashscope']
    
    for package in packages_to_check:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', '未知版本')
            print(f"✅ {package}: {version}")
        except ImportError:
            print(f"❌ {package}: 未安装")
        except Exception as e:
            print(f"⚠️  {package}: {str(e)}")
    
    print()

def check_langchain_compatibility():
    """检查LangChain兼容性"""
    print("🧪 LangChain兼容性测试...")
    print("=" * 30)
    
    try:
        from langchain.agents import create_agent
        from langchain_core.runnables.history import RunnableWithMessageHistory
        print("✅ LangChain核心组件导入成功")
        
        # 测试简单的Runnable功能
        from langchain_core.runnables import RunnableLambda
        test_runnable = RunnableLambda(lambda x: x)
        result = test_runnable.invoke("test")
        print(f"✅ Runnable基础功能正常: {result}")
        
        return True
    except Exception as e:
        print(f"❌ LangChain兼容性问题: {str(e)}")
        return False

def suggest_immediate_fix():
    """提供即时修复建议"""
    print("🛠️  即时修复建议:")
    print("=" * 20)
    print("1. 🔄 最快解决方案:")
    print("   运行: create_clean_environment.bat")
    print("   创建全新的隔离环境")
    
    print("\n2. 🔧 手动修复:")
    print("   conda create -n ai_agent_fix python=3.9 -y")
    print("   conda activate ai_agent_fix")
    print("   pip install -r requirements-stable.txt")
    
    print("\n3. 💡 临时绕过:")
    print("   修改 react_agent.py 使用 invoke 替代 stream")
    print("   （我已经为您做了这个修改）")

def run_compatibility_test():
    """运行兼容性测试"""
    print("🏃 运行兼容性测试...")
    print("=" * 25)
    
    try:
        # 测试修改后的代码
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from agent.react_agent import ReactAgent
        
        agent = ReactAgent(session_id="test_session")
        print("✅ Agent初始化成功")
        
        # 测试基础功能
        test_query = "测试查询"
        response_count = 0
        for chunk in agent.execute_stream(test_query):
            response_count += 1
            if response_count > 3:  # 限制输出长度
                break
            print(f"响应片段 {response_count}: {chunk.strip()}")
        
        print("✅ 基础功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 兼容性测试失败: {str(e)}")
        return False

if __name__ == '__main__':
    check_current_environment()
    is_compatible = check_langchain_compatibility()
    
    if not is_compatible:
        suggest_immediate_fix()
    
    print("\n" + "=" * 50)
    test_result = run_compatibility_test()
    
    if test_result:
        print("🎉 环境配置正确，可以正常使用！")
    else:
        print("💥 环境仍有问题，建议创建新环境")
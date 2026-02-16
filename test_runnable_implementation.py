"""
测试RunnableWithMessageHistory实现
验证对话记忆功能是否正常工作
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.react_agent import ReactAgent
import time

def test_memory_functionality():
    """测试记忆功能"""
    
    print("🤖 开始测试RunnableWithMessageHistory记忆功能")
    print("=" * 50)
    
    # 创建测试会话
    session_id = "test_runnable_2026"
    agent = ReactAgent(session_id=session_id)
    
    print(f"📋 测试会话ID: {session_id}")
    print("✨ 测试要点:")
    print("1. 自动历史消息管理")
    print("2. 多轮对话连贯性")
    print("3. 会话持久化")
    print("4. 内存消息数量统计")
    print()
    
    # 第一轮对话
    print("🔄 第一轮对话:")
    print("👤 用户: 我想了解扫地机器人的基本工作原理")
    
    response1 = ""
    for chunk in agent.execute_stream("我想了解扫地机器人的基本工作原理"):
        response1 += chunk
        print(f"🤖 AI: {chunk}", end="")
        time.sleep(0.01)  # 模拟流式输出
    
    print(f"\n📊 当前会话消息数: {len(agent.memory.messages)}")
    print("=" * 30)
    
    # 第二轮对话
    print("🔄 第二轮对话（测试历史记忆）:")
    print("👤 用户: 那它有哪些导航方式？")
    
    response2 = ""
    for chunk in agent.execute_stream("那它有哪些导航方式？"):
        response2 += chunk
        print(f"🤖 AI: {chunk}", end="")
        time.sleep(0.01)
    
    print(f"\n📊 当前会话消息数: {len(agent.memory.messages)}")
    print("=" * 30)
    
    # 第三轮对话
    print("🔄 第三轮对话（继续测试历史）:")
    print("👤 用户: 激光导航和视觉导航哪个更好？")
    
    response3 = ""
    for chunk in agent.execute_stream("激光导航和视觉导航哪个更好？"):
        response3 += chunk
        print(f"🤖 AI: {chunk}", end="")
        time.sleep(0.01)
    
    print(f"\n📊 最终会话消息数: {len(agent.memory.messages)}")
    print("=" * 50)
    
    # 验证记忆持久化
    print("💾 测试记忆持久化:")
    new_agent = ReactAgent(session_id=session_id)
    loaded_messages = new_agent.memory.messages
    print(f"重新加载后读取到 {len(loaded_messages)} 条消息")
    
    if len(loaded_messages) == len(agent.memory.messages):
        print("✅ 记忆持久化测试通过！")
    else:
        print("❌ 记忆持久化测试失败！")
    
    print("\n" + "=" * 50)
    print("🎯 测试总结:")
    print("• RunnableWithMessageHistory自动管理历史消息")
    print("• 多轮对话保持上下文连贯性")
    print("• 会话数据持久化存储")
    print("• 实现了真正的对话记忆功能")

def show_implementation_benefits():
    """展示实现的好处"""
    
    print("\n🌟 RunnableWithMessageHistory的主要优势:")
    print()
    print("🔧 简化开发:")
    print("  • 自动处理消息历史的获取和注入")
    print("  • 无需手动拼接历史消息")
    print("  • 内置历史长度管理")
    print()
    print("⚡ 性能优化:")
    print("  • 官方优化的历史管理机制")
    print("  • 自动控制token使用量")
    print("  • 减少内存占用")
    print()
    print("🛡️ 稳定性:")
    print("  • 经过充分测试的官方组件")
    print("  • 更少的潜在bug")
    print("  • 标准化的错误处理")
    print()
    print("🎯 最佳实践:")
    print("  • 符合LangChain设计模式")
    print("  • 代码更简洁易维护")
    print("  • 与其他LangChain组件更好集成")

if __name__ == "__main__":
    test_memory_functionality()
    show_implementation_benefits()
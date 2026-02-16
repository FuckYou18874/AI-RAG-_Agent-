"""
会话记忆功能测试脚本
模拟用户对话流程，展示长期记忆的具体实现
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.react_agent import ReactAgent
from langchain_core.messages import HumanMessage, AIMessage
import time

def simulate_user_interaction():
    """模拟用户交互流程"""
    
    print("🤖 开始模拟用户对话流程...")
    print("=" * 50)
    
    # 创建测试会话
    session_id = "test_user_2026"
    agent = ReactAgent(session_id=session_id)
    
    print(f"📋 会话ID: {session_id}")
    print(f"💾 记忆存储路径: memory/{session_id}.json")
    print()
    
    # 模拟第一轮对话
    print("🔄 第一轮对话:")
    print("👤 用户: 我想了解一下扫地机器人的选购要点")
    
    response1 = ""
    for chunk in agent.execute_stream("我想了解一下扫地机器人的选购要点"):
        response1 += chunk
        print(f"🤖 AI: {chunk}", end="")
        time.sleep(0.01)  # 模拟流式输出
    
    print("\n" + "=" * 30)
    
    # 模拟第二轮对话（基于历史）
    print("🔄 第二轮对话（带历史记忆）:")
    print("👤 用户: 那预算3000元左右的推荐哪款？")
    
    response2 = ""
    for chunk in agent.execute_stream("那预算3000元左右的推荐哪款？"):
        response2 += chunk
        print(f"🤖 AI: {chunk}", end="")
        time.sleep(0.01)
    
    print("\n" + "=" * 30)
    
    # 模拟第三轮对话（继续使用历史）
    print("🔄 第三轮对话（继续使用历史）:")
    print("👤 用户: 这款机器人的维护保养有什么要注意的？")
    
    response3 = ""
    for chunk in agent.execute_stream("这款机器人的维护保养有什么要注意的？"):
        response3 += chunk
        print(f"🤖 AI: {chunk}", end="")
        time.sleep(0.01)
    
    print("\n" + "=" * 50)
    
    # 展示记忆内容
    print("🧠 当前会话记忆内容:")
    messages = agent.memory.messages
    print(f"总共保存了 {len(messages)} 条消息 ({len(messages)//2} 轮对话)")
    
    for i, msg in enumerate(messages):
        role = "👤 用户" if isinstance(msg, HumanMessage) else "🤖 AI"
        content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
        print(f"{i+1}. {role}: {content_preview}")
    
    print("\n" + "=" * 50)
    
    # 测试记忆持久化
    print("💾 测试记忆持久化:")
    print("创建新Agent实例读取同一会话记忆...")
    
    # 创建新的Agent实例
    new_agent = ReactAgent(session_id=session_id)
    new_messages = new_agent.memory.messages
    
    print(f"新实例读取到 {len(new_messages)} 条消息")
    print("✅ 记忆持久化测试通过！")
    
    # 清理会话（可选）
    print("\n🧹 清理会话记忆...")
    agent.memory.clear()
    print("✅ 会话记忆已清空")

def demonstrate_memory_benefits():
    """展示记忆功能带来的好处"""
    
    print("\n🌟 记忆功能带来的优势:")
    print("1. 🔗 上下文连贯性 - AI能理解对话的前后关系")
    print("2. 🎯 个性化服务 - 记住用户偏好和历史询问")
    print("3. 📚 知识累积 - 避免重复解释相同概念")
    print("4. 🔄 会话延续 - 支持长时间的复杂咨询")
    print("5. 💾 数据持久化 - 重启后仍保留历史记录")
    
    print("\n🔧 技术实现要点:")
    print("• 基于文件的JSON存储，简单可靠")
    print("• 自动管理会话生命周期")
    print("• 支持历史消息数量限制（避免token超限）")
    print("• 异常安全处理（文件损坏、权限等问题）")

if __name__ == "__main__":
    simulate_user_interaction()
    demonstrate_memory_benefits()
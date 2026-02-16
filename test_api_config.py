"""
API配置测试脚本
验证API密钥是否正确配置并能正常调用
"""
import os
from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings

# 加载环境变量
load_dotenv()

def test_api_configuration():
    """测试API配置"""
    print("🔍 开始测试API配置...")
    print("=" * 50)
    
    # 检查环境变量
    api_key = os.getenv('DASHSCOPE_API_KEY')
    print(f"🔑 API密钥状态: {'✓ 已配置' if api_key and api_key != 'your_dashscope_api_key_here' else '✗ 未配置'}")
    
    if not api_key or api_key == 'your_dashscope_api_key_here':
        print("❌ 错误：请先在.env文件中配置有效的DASHSCOPE_API_KEY")
        print("💡 提示：参考 README_API_CONFIG.md 获取配置方法")
        return False
    
    print(f"📋 API密钥长度: {len(api_key)} 字符")
    print()
    
    # 测试聊天模型
    print("💬 测试聊天模型连接...")
    try:
        chat_model = ChatTongyi(
            model="qwen3-max",
            dashscope_api_key=api_key
        )
        
        # 发送简单测试消息
        response = chat_model.invoke("你好，请用一句话介绍你自己")
        print("✅ 聊天模型连接成功!")
        print(f"🤖 回复: {response.content}")
        print()
        
    except Exception as e:
        print(f"❌ 聊天模型连接失败: {str(e)}")
        return False
    
    # 测试嵌入模型
    print("🔗 测试嵌入模型连接...")
    try:
        embed_model = DashScopeEmbeddings(
            model="text-embedding-v4",
            dashscope_api_key=api_key
        )
        
        # 测试嵌入生成
        embeddings = embed_model.embed_documents(["测试文本"])
        print("✅ 嵌入模型连接成功!")
        print(f"📊 嵌入维度: {len(embeddings[0])}")
        print()
        
    except Exception as e:
        print(f"❌ 嵌入模型连接失败: {str(e)}")
        return False
    
    print("🎉 所有API配置测试通过！")
    print("🚀 现在可以正常使用大模型功能了！")
    return True

if __name__ == '__main__':
    success = test_api_configuration()
    if not success:
        exit(1)
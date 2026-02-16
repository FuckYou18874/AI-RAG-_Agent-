"""
会话记忆管理器
实现基于文件的长期会话记忆功能
"""
import os
import json
from typing import Sequence
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


class FileChatMessageHistory:
    """基于文件的聊天历史记录管理器"""
    
    def __init__(self, session_id: str, storage_path: str = None):
        """
        初始化记忆管理器
        :param session_id: 会话ID，用于区分不同用户的对话历史
        :param storage_path: 存储路径，默认为项目根目录下的memory文件夹
        """
        self.session_id = session_id
        
        # 默认存储路径
        if storage_path is None:
            storage_path = get_abs_path("memory")
            
        self.storage_path = storage_path
        # 完整的文件路径：memory/session_id.json
        self.file_path = os.path.join(self.storage_path, f"{session_id}.json")
        
        # 确保存储目录存在
        os.makedirs(self.storage_path, exist_ok=True)
        
        logger.info(f"[记忆管理]初始化会话记忆，会话ID: {session_id}, 存储路径: {self.file_path}")

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """
        添加消息到历史记录
        :param messages: 要添加的消息列表
        """
        # 获取已有的消息
        all_messages = list(self.messages)
        # 合并新消息
        all_messages.extend(messages)
        
        # 转换为字典格式便于存储
        new_messages = [message_to_dict(message) for message in all_messages]
        
        # 写入文件
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(new_messages, f, ensure_ascii=False, indent=2)
            logger.info(f"[记忆管理]成功保存{len(messages)}条消息到会话{self.session_id}")
        except Exception as e:
            logger.error(f"[记忆管理]保存消息失败: {str(e)}")

    @property
    def messages(self) -> list[BaseMessage]:
        """
        获取所有历史消息
        :return: BaseMessage对象列表
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            # 文件不存在，返回空列表
            logger.info(f"[记忆管理]会话{self.session_id}的历史记录文件不存在，返回空列表")
            return []
        except json.JSONDecodeError:
            # 文件损坏，返回空列表并记录日志
            logger.warning(f"[记忆管理]会话{self.session_id}的历史记录文件损坏")
            return []
        except Exception as e:
            logger.error(f"[记忆管理]读取历史消息失败: {str(e)}")
            return []

    def clear(self) -> None:
        """清空会话历史"""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)
            logger.info(f"[记忆管理]已清空会话{self.session_id}的历史记录")
        except Exception as e:
            logger.error(f"[记忆管理]清空历史记录失败: {str(e)}")

    def get_recent_messages(self, limit: int = 10) -> list[BaseMessage]:
        """
        获取最近的几条消息
        :param limit: 限制返回的消息数量
        :return: 最近的消息列表
        """
        all_messages = self.messages
        return all_messages[-limit:] if len(all_messages) > limit else all_messages

    def delete_session(self) -> bool:
        """
        删除整个会话记录
        :return: 删除是否成功
        """
        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
                logger.info(f"[记忆管理]已删除会话{self.session_id}的所有记录")
                return True
            return False
        except Exception as e:
            logger.error(f"[记忆管理]删除会话记录失败: {str(e)}")
            return False


class SessionManager:
    """会话管理器，管理多个用户的会话"""
    
    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or get_abs_path("memory")
        self.sessions = {}  # 缓存会话对象
        
    def get_session(self, session_id: str) -> FileChatMessageHistory:
        """
        获取指定会话的记忆管理器
        :param session_id: 会话ID
        :return: FileChatMessageHistory实例
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = FileChatMessageHistory(session_id, self.storage_path)
        return self.sessions[session_id]
    
    def list_sessions(self) -> list[str]:
        """列出所有会话ID"""
        try:
            if not os.path.exists(self.storage_path):
                return []
            
            session_files = [f for f in os.listdir(self.storage_path) if f.endswith('.json')]
            return [f[:-5] for f in session_files]  # 去掉.json后缀
        except Exception as e:
            logger.error(f"[会话管理]列出会话失败: {str(e)}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """删除指定会话"""
        if session_id in self.sessions:
            success = self.sessions[session_id].delete_session()
            if success:
                del self.sessions[session_id]
            return success
        return False


# 全局会话管理器实例
session_manager = SessionManager()

if __name__ == '__main__':
    # 测试代码
    manager = SessionManager()
    
    # 创建测试会话
    session = manager.get_session("test_user_001")
    
    # 测试添加消息
    from langchain_core.messages import HumanMessage, AIMessage
    
    test_messages = [
        HumanMessage(content="你好，我想了解一下扫地机器人的使用方法"),
        AIMessage(content="您好！我很乐意为您介绍扫地机器人的使用方法...")
    ]
    
    session.add_messages(test_messages)
    
    # 测试获取消息
    recent_msgs = session.get_recent_messages(5)
    print(f"获取到{len(recent_msgs)}条消息")
    
    # 测试列出所有会话
    all_sessions = manager.list_sessions()
    print(f"所有会话: {all_sessions}")
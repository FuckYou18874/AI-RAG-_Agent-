import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_conf

# 加载环境变量
load_dotenv()

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        # 设置DashScope API密钥
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if not api_key or api_key == 'your_dashscope_api_key_here':
            raise ValueError("请在.env文件中配置有效的DASHSCOPE_API_KEY")
        
        return ChatTongyi(
            model=rag_conf["chat_model_name"],
            dashscope_api_key=api_key
        )


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        # 设置DashScope API密钥
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if not api_key or api_key == 'your_dashscope_api_key_here':
            raise ValueError("请在.env文件中配置有效的DASHSCOPE_API_KEY")
            
        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"],
            dashscope_api_key=api_key
        )


chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()
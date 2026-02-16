from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import (rag_summarize, get_weather, get_user_location, get_user_id,
                                     get_current_month, fetch_external_data, fill_context_for_report)
from utils.memory_manager import session_manager
from utils.logger_handler import logger


class ReactAgent:
    def __init__(self, session_id: str = "default_session"):
        self.session_id = session_id
        self.memory = session_manager.get_session(session_id)
        
        tools = [rag_summarize, get_weather, get_user_location, get_user_id,
                 get_current_month, fetch_external_data, fill_context_for_report]
        
        system_prompt = load_system_prompts()
        
        self.agent = create_react_agent(
            model=chat_model,
            tools=tools,
            prompt=system_prompt
        )

    def execute_stream(self, query: str):
        current_message = HumanMessage(content=query)
        
        logger.info(f"[Agent执行]会话ID: {self.session_id}, 当前问题: {query[:50]}...")
        
        try:
            logger.info("[Agent执行]开始调用模型...")
            
            history_messages = list(self.memory.messages)
            history_messages.append(current_message)
            
            response = self.agent.invoke(
                {"messages": history_messages}
            )
            
            logger.info(f"[Agent执行]模型响应类型: {type(response)}")
            
            if 'messages' in response and response['messages']:
                latest_message = response['messages'][-1]
                if hasattr(latest_message, 'content') and latest_message.content:
                    self.memory.add_messages([current_message, latest_message])
                    yield latest_message.content.strip() + "\n"
            elif isinstance(response, str):
                yield response.strip() + "\n"
            else:
                logger.warning(f"[Agent执行]未知响应类型: {type(response)}")
                yield "系统正在处理您的请求..."
                
        except Exception as e:
            logger.error(f"[Agent执行]执行出错: {str(e)}", exc_info=True)
            yield "抱歉，系统暂时无法处理您的请求。错误信息：" + str(e)


if __name__ == '__main__':
    agent = ReactAgent()

    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)
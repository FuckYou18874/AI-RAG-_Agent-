import time
import uuid

import streamlit as st
from agent.react_agent import ReactAgent

# 标题
st.title("智扫通机器人智能客服")
st.divider()

# 会话管理
if "session_id" not in st.session_state:
    # 为每个用户生成唯一的会话ID
    st.session_state["session_id"] = str(uuid.uuid4())

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent(session_id=st.session_state["session_id"])

if "message" not in st.session_state:
    st.session_state["message"] = []

# 显示当前会话ID（调试用）
st.sidebar.markdown(f"**会话ID:** {st.session_state['session_id'][:8]}...")

# 会话控制按钮
if st.sidebar.button("开始新会话"):
    # 生成新的会话ID
    st.session_state["session_id"] = str(uuid.uuid4())
    st.session_state["message"] = []
    st.session_state["agent"] = ReactAgent(session_id=st.session_state["session_id"])
    st.rerun()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):

            for chunk in generator:
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        
        # 显示记忆状态
        memory_status = f"📝 已保存到会话记忆 ({len(st.session_state['agent'].memory.messages)//2}轮对话)"
        st.caption(memory_status)
        
        st.rerun()

from flask import Flask, request, jsonify
from agent.react_agent import ReactAgent
import uuid

app = Flask(__name__)

# 全局机器人实例
robot_agent = ReactAgent(session_id="api_default")


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')

        if not message:
            return jsonify({'error': '消息不能为空'}), 400

        # 让机器人回答
        response_chunks = []
        for chunk in robot_agent.execute_stream(message):
            response_chunks.append(chunk)

        full_response = ''.join(response_chunks)

        return jsonify({
            'response': full_response,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'robot-api'})


if __name__ == '__main__':
    print("🤖 机器人API服务启动中...")
    print("访问地址: http://localhost:5000")
    print("聊天接口: POST http://localhost:5000/chat")
    print("健康检查: GET http://localhost:5000/health")
    app.run(host='0.0.0.0', port=5000)

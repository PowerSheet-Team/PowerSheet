from flask import Flask, render_template
from flask_socketio import SocketIO
from analysis import Analysis
from llm.impl import llm_cpu, llm_api

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins='*')

llm = llm_api.LLM_API()

@socketio.on('message')
def handle_message(msg):
    print('Received message: ', msg)
    analysis = Analysis(msg)
    context = llm.getContext()
    print(analysis.gen_query())
    reply = context.query(analysis.gen_query())
    print(reply)
    cell_candidate = analysis.apply_reply(reply)
    reply = {
        "status": "ok",
        "range": analysis.outputSection.range,
        "candidate": cell_candidate,
    }

    print(reply)

    socketio.emit('message', reply)  # 广播消息给所有连接的客户端


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)

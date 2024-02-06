from flask import Flask, render_template
from flask_socketio import SocketIO
from analysis import Analysis

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins='*')


@socketio.on('message')
def handle_message(msg):
    print('Received message: ', msg)
    socketio.emit('message', msg)  # 广播消息给所有连接的客户端


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)

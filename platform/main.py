from flask import Flask, render_template
from flask_socketio import SocketIO
from analysis import Analysis
from llm.impl import llm_cpu, llm_api

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

llm = llm_api.LLM_API()

last_context = None


def handle_autofill(msg):
    analysis = Analysis(msg)
    context = llm.getContext()
    last_context = context
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

    socketio.emit('message', reply)

def handle_feedback(msg):
    analysis = Analysis(msg)
    context = last_context
    reply = context.query(msg["feedbackMsg"])
    print(reply)
    cell_candidate = analysis.apply_reply(reply)
    reply = {
        "status": "ok",
        "range": analysis.outputSection.range,
        "candidate": cell_candidate,
    }

    print(reply)

    socketio.emit('message', reply)


@socketio.on('message')
def handle_message(msg):
    global last_context
    print('Received message: ', msg)
    if msg["type"] == "fill":
        handle_autofill(msg)
    elif msg["type"] == "feedback":
        handle_feedback(msg)

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)

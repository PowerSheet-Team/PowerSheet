from flask import Flask, render_template
from flask_socketio import SocketIO
from analysis import Analysis
from llm.impl import llm_cpu, llm_api

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

llm = llm_api.LLM_API()

last_context = None
last_analysis = None


def handle_autofill(msg):
    global last_context
    global last_analysis
    analysis = Analysis(msg)
    context = llm.getContext()
    last_context = context
    last_analysis = analysis
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
    context = last_context
    analysis = last_analysis
    reply = context.query(f"No I does not mean that, I want " + msg["feedbackMsg"])
    print(reply)
    cell_candidate = analysis.apply_reply(reply)
    reply = {
        "status": "ok",
        "range": analysis.outputSection.range,
        "candidate": cell_candidate,
    }

    print(reply)

    socketio.emit('message', reply)

def handle_rangesel(msg):
    context = llm.getContext()
    query = Analysis.gen_range_sel_query(msg["description"])
    reply = context.query(query)
    print(reply)
    code = Analysis.apply_code(reply)
    print(code)
    reply = {
        "status": "ok",
        "code": code,
        "range": msg["inputRange"]
    }
    print(reply)
    socketio.emit('message', reply)

def handle_summary(msg):
    global last_context
    global last_analysis
    analysis = Analysis(msg)
    context = llm.getContext()
    last_context = context
    last_analysis = analysis
    print(analysis.gen_summary_query())
    reply = context.query(analysis.gen_summary_query())
    print(reply)
    reply = {
        "status": "ok",
        "reply": reply
    }

    print(reply)

    socketio.emit('message', reply)

def handle_formula_exp(msg):
    global last_context
    global last_analysis
    analysis = Analysis(msg)
    context = llm.getContext()
    last_context = context
    last_analysis = analysis
    print(analysis.gen_exp_explain_query())
    reply = context.query(analysis.gen_exp_explain_query())
    print(reply)
    reply = {
        "status": "ok",
        "reply": reply
    }

    print(reply)

    socketio.emit('message', reply)

def handle_formula_pbe(msg):
    global last_context
    global last_analysis
    analysis = Analysis(msg)
    context = llm.getContext()
    last_context = context
    last_analysis = analysis
    print(analysis.gen_query())
    reply = context.query(analysis.gen_formula_pbe_query())
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
    elif msg["type"] == "summary":
        handle_summary(msg)
    elif msg["type"] == "formula_exp":
        handle_formula_exp(msg)
    elif msg["type"] == "formula_pbe":
        handle_formula_pbe(msg)
    elif msg["type"] == "range_sel":
        handle_rangesel(msg)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)

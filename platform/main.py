from flask import Flask, render_template
from flask_socketio import SocketIO
from analysis import Analysis
from llm.impl import llm_api

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

llm = llm_api.LLM_API()


class ContextManager:
    def __init__(self):
        self.context = None
        self.analysis = None

    def set_last_context(self, context):
        self.context = context

    def set_last_analysis(self, analysis):
        self.analysis = analysis

    def get_last_context(self):
        return self.context

    def get_last_analysis(self):
        return self.analysis


context_manager = ContextManager()


def handle_autofill(msg):
    analysis = Analysis(msg)
    context = llm.getContext()
    context_manager.set_last_context(context)
    context_manager.set_last_analysis(analysis)
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
    context = context_manager.get_last_context()
    analysis = context_manager.get_last_analysis()
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
        "type": "rangesel",
        "status": "ok",
        "code": code,
        "range": msg["inputRange"]
    }
    print(reply)
    socketio.emit('message', reply)


def handle_summary(msg):
    analysis = Analysis(msg)
    context = llm.getContext()
    context_manager.set_last_context(context)
    context_manager.set_last_analysis(analysis)
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
    analysis = Analysis(msg)
    context = llm.getContext()
    context_manager.set_last_context(context)
    context_manager.set_last_analysis(analysis)
    print(analysis.gen_exp_explain_query())
    reply = context.query(analysis.gen_exp_explain_query())
    print(reply)
    reply = {
        "status": "ok",
        "reply": reply
    }

    print(reply)

    socketio.emit('message', reply)


def handle_batchproc(msg):
    context = llm.getContext()
    query = Analysis.gen_batchproc_query(msg["description"])
    reply = context.query(query)
    print(reply)
    code = Analysis.apply_code(reply)
    print(code)
    reply = {
        "type": "batchproc",
        "status": "ok",
        "code": code,
        "range": msg["inputRange"]
    }
    print(reply)
    socketio.emit('message', reply)


def handle_formula_pbe(msg):
    analysis = Analysis(msg)
    context = llm.getContext()
    context_manager.set_last_context(context)
    context_manager.set_last_analysis(analysis)
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


def handle_create_visual(msg):
    context = llm.getContext()
    analysis = Analysis(msg)
    query = analysis.gen_create_visual_query()
    reply = context.query(query)
    print(reply)
    title, type = analysis.apply_create_visual(reply)
    reply = {
        "type": "create_visual",
        "status": "ok",
        "range": analysis.inputSection.range,
        "title": title,
        "chart_type": type
    }
    print(reply)
    socketio.emit('message', reply)


def handle_formula_chk(msg):
    context = llm.getContext()
    analysis = Analysis(msg)
    query = analysis.gen_formula_chk_query()
    reply = context.query(query)
    warns, passes = analysis.apply_formula_chk(reply)
    infos = []
    for warn in warns:
        infos.append({"intent": "warning", "info": warn})
    for pass_ in passes:
        infos.append({"intent": "success", "info": pass_})
    print(reply)
    reply = {
        "type": "formula_chk",
        "status": "ok",
        "info": infos,
    }
    print(reply)
    socketio.emit('message', reply)


@socketio.on('message')
def handle_message(msg):
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
    elif msg["type"] == "batchproc":
        handle_batchproc(msg)
    elif msg["type"] == "formula_chk":
        handle_formula_chk(msg)
    elif msg["type"] == "create_visual":
        handle_create_visual(msg)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)

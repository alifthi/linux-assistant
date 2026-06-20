from linux_assistant.graph.graph import build_graph
from linux_assistant.utils.dicts import AgentState
from linux_assistant.utils.console_utils import console_utils
from linux_assistant.utils.config_handler import config

def run_app():
    model_config = config()
    app = build_graph(model_config)
    console = console_utils(model_config)

    state: AgentState = {"messages": [], "logger": console}

    console.release_banner()

    while True:
        input_text = console.get_user_input()
        if input_text == "exit" or input_text == "/quit":
            break
        
        state["messages"].append({
            "role": "user",
            "content": input_text
        })

        state = app.invoke(state)
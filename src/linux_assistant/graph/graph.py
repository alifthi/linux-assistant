from linux_assistant.graph.nodes import shell_node, prepare_shell_code,\
                        tool_select, prepare_tool_prompt, prepare_search_query, search_tools
from linux_assistant.utils.dicts import AgentState
from linux_assistant.models.model_nodes import model_nodes
from linux_assistant.utils.config_handler import config
from langgraph.graph import StateGraph, START,END

def build_graph(model_config: config) -> StateGraph:
    ''' This function builds graph '''
    call_model = model_nodes(model_config)
    search = search_tools()
    graph = StateGraph(AgentState)
    graph.set_entry_point('call_model')
    graph.add_node('call_model', call_model.call_model)
    graph.add_node('prepare_tool_prompt', prepare_tool_prompt)
    graph.add_node('prepare_shell_code',prepare_shell_code)
    graph.add_node('shell_node', shell_node)
    graph.add_conditional_edges(
        "call_model",
        tool_select,
        {'shell_node': 'prepare_shell_code', "search_node": "prepare_search_query" ,"nothing": END}
    )
    graph.add_node('prepare_search_query', prepare_search_query)
    graph.add_node('search_node', search.search_node)
    graph.add_edge('prepare_search_query', 'search_node')
    graph.add_edge('search_node', 'call_model')
    graph.add_edge('prepare_shell_code', 'shell_node')
    graph.add_edge('shell_node', 'prepare_tool_prompt')
    graph.add_edge('prepare_tool_prompt','call_model')
    app = graph.compile()
    return app
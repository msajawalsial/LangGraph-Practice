from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message: str


def greeter_function(state: AgentState) -> AgentState:
    """Node to add greeting message to the state"""
    state["message"] = f"Hey {state['message']}, how is your day going?"
    return state


graph = StateGraph(AgentState)
graph.add_node("greeter", greeter_function)
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()

result = app.invoke({"message": "Alice"})
print(result["message"])

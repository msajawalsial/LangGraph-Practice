from typing import TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    compliment: str


def compliment_function(state: AgentState) -> AgentState:
    """Node to add a compliment to the state"""
    state["compliment"] = f"{state['name']}, you are doing an amazing job learning LangGraph!"
    return state


graph = StateGraph(AgentState)
graph.add_node("complimentor", compliment_function)
graph.set_entry_point("complimentor")
graph.set_finish_point("complimentor")

app = graph.compile()

result = app.invoke({"name": "Alice"})
print(result["compliment"])

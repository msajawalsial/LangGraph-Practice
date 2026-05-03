from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: int
    result: str


def first_node(state: AgentState) -> AgentState:
    """First processing node. Adds a greeting."""
    state["result"] = f"Hi {state['name']}!"
    return state

def second_node(state: AgentState) -> AgentState:
    """Second processing node. Adds age information."""
    state["result"] += f" You are {state['age']} years old."
    return state

graph = StateGraph(AgentState)
graph.add_node("first", first_node)
graph.add_node("second", second_node)
graph.set_entry_point("first")
graph.set_finish_point("second")
graph.add_edge("first", "second")

app = graph.compile()
app.invoke({"name": "Alice", "age": 30})
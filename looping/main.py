from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from random import randint

class AgentState(TypedDict):
    name: str
    numbers: List[int]
    count: int

def add_greeting(state: AgentState) -> AgentState:
    """This node adds greeting to the name."""
    state["count"] = 0
    state["name"] = f"Hello, {state['name']}!"
    return state

def add_number(state: AgentState) -> AgentState:
    """This node adds a random number to the list of numbers."""
    state["numbers"].append(randint(1, 100))
    state["count"] += 1
    return state

def decide_next_node(state: AgentState) -> str:
    """Decides the next node based on the count of numbers added."""
    if state["count"] < 5:
        return "loop"
    return "terminate"


graph = StateGraph(AgentState)
graph.add_node("greeting", add_greeting)
graph.add_node("number", add_number)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "number")
graph.add_conditional_edges(
    "number",
    decide_next_node,
    {
        "loop": "number",
        "terminate": END
    }
)

app = graph.compile()
result = app.invoke({"name": "Alice", "numbers": []})
print(result)
app.get_graph().draw_png("graph.png")

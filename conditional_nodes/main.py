from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    num1: int
    num2: int
    operation: str
    result: int

def adder(state: AgentState) -> AgentState:
    """This node adds two numbers and stores the result."""
    state["result"] = state["num1"] + state["num2"]
    return state

def subtractor(state: AgentState) -> AgentState:
    """This node subtracts two numbers and stores the result."""
    state["result"] = state["num1"] - state["num2"]
    return state

def decide_next_node(state: AgentState) -> str:
    """Decides the next node based on the operation."""
    if state["operation"] == "+":
        return "adder"
    elif state["operation"] == "-":
        return "subtractor"
    return "unknown"

graph = StateGraph(AgentState)

graph.add_node("router", lambda state: state)
graph.add_node("adder", adder)
graph.add_node("subtractor", subtractor)

graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "adder": "adder",
        "subtractor": "subtractor",
        "unknown": END
    }
)
graph.add_edge("adder", END)
graph.add_edge("subtractor", END)

app = graph.compile()
addition_result = app.invoke({"num1": 5, "num2": 3, "operation": "+"})
print(addition_result)

subtraction_result = app.invoke({"num1": 5, "num2": 3, "operation": "-"})
print(subtraction_result)

invalid_result = app.invoke({"num1": 5, "num2": 3, "operation": "*"})
print(invalid_result)

app.get_graph().draw_png("graph.png")
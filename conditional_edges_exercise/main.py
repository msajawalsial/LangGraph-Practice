from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    num1: int
    num2: int
    op1: str
    res1: int
    num3: int
    num4: int
    op2: str
    res2: int


def adder1(state: AgentState) -> AgentState:
    """This node adds num1 and num2 and stores the result in res1."""
    state["res1"] = state["num1"] + state["num2"]
    return state

def adder2(state: AgentState) -> AgentState:
    """This node adds num3 and num4 and stores the result in res2."""
    state["res2"] = state["num3"] + state["num4"]
    return state

def subtractor1(state: AgentState) -> AgentState:
    """This node subtracts num1 and num2 and stores the result in res1."""
    state["res1"] = state["num1"] - state["num2"]
    return state

def subtractor2(state: AgentState) -> AgentState:
    """This node subtracts num3 and num4 and stores the result in res2."""
    state["res2"] = state["num3"] - state["num4"]
    return state

def decide_next_node_1(state: AgentState) -> str:
    """Decides the next node based on op1."""
    if state["op1"] == "+":
        return "adder1"
    elif state["op1"] == "-":
        return "subtractor1"
    return "unknown"

def decide_next_node_2(state: AgentState) -> str:
    """Decides the next node based on op2."""
    if state["op2"] == "+":
        return "adder2"
    elif state["op2"] == "-":
        return "subtractor2"
    return "unknown"

graph = StateGraph(AgentState)
graph.add_node("router1", lambda state: state)
graph.add_node("router2", lambda state: state)
graph.add_node("adder1", adder1)
graph.add_node("adder2", adder2)
graph.add_node("subtractor1", subtractor1)
graph.add_node("subtractor2", subtractor2)

graph.add_edge(START, "router1")
graph.add_conditional_edges(
    "router1",
    decide_next_node_1,
    {
        "adder1": "adder1",
        "subtractor1": "subtractor1",
        "unknown": "router2"
    }
)
graph.add_edge("adder1", "router2")
graph.add_edge("subtractor1", "router2")
graph.add_conditional_edges(
    "router2",
    decide_next_node_2,
    {
        "adder2": "adder2",
        "subtractor2": "subtractor2",
        "unknown": END
    }
)
graph.add_edge("adder2", END)
graph.add_edge("subtractor2", END)

app = graph.compile()
result = app.invoke({
    "num1": 5,
    "num2": 3,
    "op1": "+",
    "num3": 10,
    "num4": 4,
    "op2": "-"
})
print(result)
app.get_graph().draw_png("graph.png")


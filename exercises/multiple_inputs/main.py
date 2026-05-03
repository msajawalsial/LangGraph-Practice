from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    operation: str
    result: int


def calculate(state: AgentState) -> AgentState:
    """Handles addition and multiplication operations and stores the result."""
    if state["operation"] == "+":
        state["result"] = sum(state["values"])
    elif state["operation"] == "*":
        state["result"] = 1
        for v in state["values"]:
            state["result"] *= v
    else:
        state["result"] = None
    return state

graph = StateGraph(AgentState)
graph.add_node("calculator", calculate)
graph.set_entry_point("calculator")
graph.set_finish_point("calculator")
app = graph.compile()

result = app.invoke({"values": [1, 2, 3, 4, 5], "operation": "z"})["result"]
print(result)


from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str


def process_values(state: AgentState) -> AgentState:
    """This function calculates the sum of values and stores the response made of name and sum of values into result"""
    state["result"] = f"{state['name']}, the sum of your values is {sum(state['values'])}."
    return state

graph = StateGraph(AgentState)
graph.add_node("processor", process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()


result = app.invoke({"name": "Alice", "values": [1, 2, 3, 4, 5]})

print(result)

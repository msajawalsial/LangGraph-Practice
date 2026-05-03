from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from random import randint

class AgentState(TypedDict):
    player_name: str
    guesses: List[int]
    upper_bound: int
    lower_bound: int
    actual_number: int
    guess_count: int


def setup(state: AgentState) -> AgentState:
    state['guesses'] = []
    state['upper_bound'] = 20
    state['lower_bound'] = 1
    state['actual_number'] = randint(1, 20)
    state['guess_count'] = 0
    return state

def guess(state: AgentState) -> AgentState:
    guess = (state['upper_bound'] + state['lower_bound']) // 2
    state['guesses'].append(guess)
    state['guess_count'] += 1
    return state

def hint(state: AgentState) -> AgentState:
    last_guess = state['guesses'][-1]
    if last_guess < state['actual_number']:
        state['lower_bound'] = last_guess + 1
    elif last_guess > state['actual_number']:
        state['upper_bound'] = last_guess - 1
    return state

def decide_next_node(state: AgentState) -> str:
    last_guess = state['guesses'][-1]
    if last_guess == state['actual_number'] or state['guess_count'] == 7:
        return "terminate"
    else:
        return "guess"


graph = StateGraph(AgentState)
graph.add_node("setup", setup)
graph.add_node("guess", guess)
graph.add_node("hint", hint)

graph.add_edge(START, "setup")
graph.add_edge("setup", "guess")
graph.add_edge("guess", "hint")
graph.add_conditional_edges(
    "hint",
    decide_next_node,
    {
        "guess": "guess",
        "terminate": END
    }
)
app = graph.compile()
result = app.invoke(AgentState(
    player_name="Sajawal",
))
print(result)
app.get_graph().draw_png("graph.png")
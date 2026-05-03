import os
from typing import TypedDict, List, Union
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def process(state: AgentState) -> AgentState:
    """Processes the agent state and generate a response."""
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}\n")
    state["messages"].append(AIMessage(content=response.content))
    print("Conversation history:", state["messages"])
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
app = graph.compile()

conversation = []

user_input = input("Enter: ")

while user_input.lower() != "exit":
    conversation.append(HumanMessage(content=user_input))
    llm_response = app.invoke({"messages": conversation})
    conversation = llm_response["messages"]
    user_input = input("Enter: ")
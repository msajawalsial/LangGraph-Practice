from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}\n")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
app = graph.compile()

user_input = input("Enter: ")
while user_input != "exit":
    app.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")

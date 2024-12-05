"""
Simple react agent architecture based on simple graph and chains and routers example with tools
ReAct has 3 components:
- Act
- Observe
- Reason

In this case, the model will continue to call tools until the task is finished. We send the output of the call back to the LLM.
## Structure:

START -> assistant_node
assistant_node -> tools
assistant_node -> END
tools -> assistant_node
tools -> END

Notes: 
- Using Prebuilt ToolNode, tools_condition and MessageState, but probably would prefer to write their behaviour explicitly
- LLMs, nodes and tools could be anything, but using Langchain to keep within same framework logic.
"""
import sys
from typing import List, TypedDict
from dotenv import load_dotenv
from pprint import pprint
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import Tool

# Copied from chains/routers files
load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

# Tools
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b

def add(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b

llm_with_tools = llm.bind_tools([multiply, add])

def assistant_node(state: MessagesState):
    new_msg = llm_with_tools.invoke(state["messages"])
    return {"messages": [new_msg]}

def build_graph(tools=[multiply, add]) -> StateGraph:
    builder = StateGraph(MessagesState)
    builder.add_node("assistant_node", assistant_node)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "assistant_node")
    builder.add_edge("assistant_node", END)
    # builder.add_edge("tools", END) The design has tool ending it, but i want it to always go back to assistant
    builder.add_edge("tools", "assistant_node")
    builder.add_conditional_edges("assistant_node", tools_condition) # decides if go to tools node or END

    graph = builder.compile()
    return graph

if __name__ == "__main__":
    print("This agent will process your request and exit. It can do addition and multiplication.")
    print(len(sys.argv))
    if len(sys.argv) <= 1:
        print("To ask a question, pass a string when executing the file: `python agent-langraph.py 'Add 3 and 4, then multiply by 2.' ")
        query ="Add 3 and 4, then multiply by 2."
    else:
        query = str(sys.argv[1])
    graph = build_graph()
    start_state = {"messages":[HumanMessage(content=query)]}

    messages = graph.invoke(start_state)
    for msg in messages["messages"]:
        msg.pretty_print()


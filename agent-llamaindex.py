import sys
from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool

load_dotenv()

def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b


multiply_tool = FunctionTool.from_defaults(fn=multiply)


def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b


add_tool = FunctionTool.from_defaults(fn=add)


if __name__ == "__main__":
    print("This agent will process your request and exit. It can do any maths")
    print(len(sys.argv))
    if len(sys.argv) <= 1:
        print("To ask a question, pass a string when executing the file: `python agent-langraph.py 'Add 3 and 4, then multiply by 2.' ")
        query ="Add 3 and 4, then multiply by 2."
    else:
        query = str(sys.argv[1])

    llm = OpenAI(model="gpt-4o-mini")

    agent = ReActAgent.from_tools([multiply_tool, add_tool], llm=llm, verbose=True)

    response = agent.chat(query)
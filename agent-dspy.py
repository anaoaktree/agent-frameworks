"""
DSPy version of react agent

"""
import sys
import dspy

# experimenting with Python Repl tool - works well
def evaluate_math(expression: str):
    """
    Executes math expressions in Python interpreter
    Args:
        expression: Math expression in Python
    """
    return dspy.PythonInterpreter({}).execute(expression)


if __name__ == "__main__":
    print("This agent will process your request and exit. It can do any maths")
    print(len(sys.argv))
    if len(sys.argv) <= 1:
        print("To ask a question, pass a string when executing the file: `python agent-langraph.py 'Add 3 and 4, then multiply by 2.' ")
        query ="Add 3 and 4, then multiply by 2."
    else:
        query = str(sys.argv[1])
    lm = dspy.LM('openai/gpt-4o-mini')
    dspy.configure(lm=lm)
    react = dspy.ReAct("question -> answer: float", tools=[evaluate_math])
    pred = react(question=query)
    print(pred.reasoning)
    print(pred.answer)
    print(dspy.inspect_history(n=3))
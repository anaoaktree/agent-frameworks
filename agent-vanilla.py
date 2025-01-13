
import re
from typing import List, Dict
import anthropic

class TerminalColors:
    GREEN = '\033[32m'
    MAGENTA = '\033[35m'
    YELLOW= '\033[33m'
    RESET = '\033[0m'


# API key can be obtained on Anthropic's developer console. 
# Keep your API Key private
claude = anthropic.Anthropic(
    api_key="sk-")

# ReAct System prompt, based on https://til.simonwillison.net/llms/python-react-pattern
SYSTEM_PROMPT="""
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
OPTIONAL - Use Action to run one of the actions available to you - then return PAUSE.
OPTIONAL - Observation will be the result of running those actions.
... (this Thought/Action/Observation can repeat N times)

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

Example session:

Question: 87 * 91
Thought: I should use calculate
Action: calculate: 87*91
PAUSE

You will be called again with this:

Observation: The result of the calculation is 7917.

You then output: 7917.

"""



def get_claude_response(conversation: List[Dict]) -> str:
    """
    Calls anthropic API to generate text.
    """
    claude_message = claude.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=conversation
    )
    return claude_message.content[0].text


def calculate(expression:str):
    return eval(expression)


if __name__ == "__main__":
    observation = ""
    conversation = []
    while True:
        # prompt the user to write a question or sends observation (result of action) back to claude
        user_query = observation or input(TerminalColors.MAGENTA + "ana >> ") 
        observation = "" # if there was an observation, reset
        # append user prompt to the conversation (anthropic compatible format)
        conversation += [{'role': 'user', 'content': [{"type":"text","text":user_query}]}] 

        # get response from claude LLM
        claude_reply = get_claude_response(conversation)
        # show claude response
        print(TerminalColors.GREEN + "claude >> ", claude_reply)
        # append claude response to the conversation - role = assistant (anthropic compatible format)
        conversation += [{'role': 'assistant', 'content': [{"type":"text","text":claude_reply}]}] 

        # ReAct code block to check for actions
        action_re = re.compile('^Action: (\w+): (.*)$')
        # Checks if there is an action to run using the above regular expression: looks for the pattern `Action:` followed by inputs
        actions = [action_re.match(a) for a in claude_reply.split('\n') if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action!= "calculate":
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            result = calculate(action_input)
            observation = "Observation: {}".format(result)
            print(TerminalColors.YELLOW + "observation >> ", observation)






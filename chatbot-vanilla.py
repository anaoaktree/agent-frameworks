
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
    api_key="sk-ant-")


def get_claude_response(conversation: List[Dict]) -> str:
    """
    Calls anthropic API to generate text.
    """
    claude_message = claude.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        system="You are a world-class AI Assistant",
        messages=conversation
    )
    return claude_message.content[0].text


if __name__ == "__main__":
    conversation = []
    while True:
        # prompt the user to write a question
        user_query = input(TerminalColors.MAGENTA + "ana >> ") 
        # append user prompt to the conversation (anthropic compatible format)
        conversation += [{'role': 'user', 'content': [{"type":"text","text":user_query}]}] 

        # get response from claude LLM
        claude_reply = get_claude_response(conversation)
        # show claude response
        print(TerminalColors.GREEN + "claude >> ", claude_reply)
        # append claude response to the conversation - role = assistant (anthropic compatible format)
        conversation += [{'role': 'assistant', 'content': [{"type":"text","text":claude_reply}]}] 


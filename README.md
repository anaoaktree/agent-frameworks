# React Agents - Langgraph, LLamaindex and DSPy
A comparative analysis of building ReAct (Reasoning + Acting) agents using LangGraph, LlamaIndex, and DSPy frameworks. This project aims to evaluate different approaches for implementing autonomous coding agents, with the ultimate goal of developing a Python project starter agent. In addition to these frameworks, a vanilla Python agent will be used as baseline comparison.
Each implementation focuses on a simple use case: creating a "Hello World" Flask application to evaluate framework capabilities and compare implementation approaches.

## Evaluation criteria
The primary aspects being evaluated are:

### 1. Control Flow Flexibility

- How rigid or flexible is the interaction logic?
- What control patterns are supported?
- How easy is it to modify the agent's behavior?


### 2. Tool Integration

- Code generation
- File system operations
- Terminal command execution
- Ease of adding new tools

### 3. Human in the loop

- Introduce human feedback in control flow


## Current Status
- Basic ReAct agent with simple tools for Langgraph, DSPy and LLamaindex

### Langgraph
My Notes: 
- I like the use of the graph and it seems like it is a good option for control flow flexibility.
- The current version (calculator) handles well non-math questions (like "Hello") since it defaults to assistant.
- Can use the graph concept for contrl flow and LLMs/Tools from other frameworks
- Has Langsmith for observability

### DSPy
My Notes: 
- I like the modularity and simplicity of coding. Cheated a bit and used their built-in react
- The current version (calculator) doesn't handle well non-math questions, which shows some inflexibility - would probably need to write a bespoke signature and/or implement the react agent from scratch.

### Llamaindex
My Notes: 
- Also used default react agent - works well with tool use and when it doesn't need to use tools.

### Vanilla
TODO

## To Do Next
- Complete basic agent implementations across all frameworks
- Implement necessary tools interfaces
- Add performance metrics and comparisons
- Improve README

## How to run

- Add a .env file with OPENAI_API_KEY
- Create a virtual env and install the requirements for the framework OR run `source ./setup.sh <framework>`
- run the agent file





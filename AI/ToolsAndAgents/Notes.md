https://smith.langchain.com/hub

Here we have langchain hub those are helpful for already commited few prompts

# Tools and Agents
Tools are interfaces that an agent, chain, or LLM can use to interact with the world. They combine a few things:

- The name of the tool
- A description of what the tool is
- JSON schema of what the inputs to the tool are
- The function to call
- Whether the result of a tool should be returned directly to the user

# Agents
The core idea of agents is to use a language model to choose a sequence of actions to take. In chains, a sequence of actions is hardcoded (in code). In agents, a language model is used as a reasoning engine to determine which actions to take and in which order.
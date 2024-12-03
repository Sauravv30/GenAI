# import openai
from langchain.agents import initialize_agent, Tool, AgentType, create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_groq import ChatGroq

# Initialize the LLM
# llm = OpenAI(openai_api_key='your-openai-api-key')
llm = ChatGroq(model="Llama3-8b-8192", temperature=0.5,
               api_key="")

# Initialize the web search tool (DuckDuckGo in this case)
search_tool = DuckDuckGoSearchResults()

# session_id = "default"
store = {}
previous_input = ""


def should_repeat_conversation(user_input):
    """Check if the user is repeating previous conversational questions."""
    global previous_input
    if user_input == previous_input:
        return True
    previous_input = user_input
    return False





def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
        print(f"Created new chat history for {session_id}")
    return store[session_id]


# Define tools that LLM can use
tools = [
    Tool(
        name="LLM Search",
        func=llm.invoke,
        description="Use this tool to perform basic LLM search."
    )
    # ),
    # Tool(
    #     name="Web Search",
    #     func=search_tool.run,
    #     description="Use this tool to perform web searches when the model doesn't know the answer."
    # ),
]


# Define the agent
# agent = initialize_agent(
#     tools,
#     llm,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

def execute():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",
             "You are a helpful assistant. For each query, you must use the tools in the exact order they are provided. "
             "You must use the first tool first, then the second tool, then the third, and so on, in the same order. "
             "Do not skip any tool or change the order. Only move to the next tool if the previous tool has failed to provide a useful answer. "
             "If a tool fails, you may try the next one, but always maintain the order."
             ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    # Create the agent (with the history-aware retriever and the prompt)

    memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=1)
    # Return an agent executor with memory integration (this will execute the agent with history)
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_chain = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_interations=2,
        handle_parsing_errors=str
        # early_stopping_method="generate"
    )
    print(f"Tools -> {agent_chain.tools}")

    return RunnableWithMessageHistory(
        agent_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="output"
    )

# Simple set of phrases that can be handled directly
common_greetings = ["hello", "hi", "how are you", "is there something i can help you with", "thank you", "please", "goodbye"]

def should_use_llm_only(user_input):
    """Check if the input is a common conversational query."""
    return user_input.lower() in common_greetings

def handle_input(user_input):
    if should_use_llm_only(user_input):
        return llm_chain.run(user_input)
    elif should_repeat_conversation(user_input):
        return "Let's continue the conversation. What else would you like to know?"
    else:
        return web_search_tool.run(user_input)

# Function to ask the LLM
def ask_with_search(query):
    return execute().invoke({"input": query},
                            config={"configurable": {"session_id": "default"}})
    # return response


# Example usage
# query = "Who was Ratan Tata ?"
user_input = input("Enter query: ")
while True:
    if user_input == "End":
        break
    else:
        response = ask_with_search(user_input)
        print(response)

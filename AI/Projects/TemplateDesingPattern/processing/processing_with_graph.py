from typing import TypedDict, Annotated

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import Tool
from langchain_groq import ChatGroq

from constants import app_constants
from langchain_ollama import OllamaLLM
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import tools_condition
from prompts.aiprompts import contextualize_q_system_prompt, system_prompt, system_tool_prompt
from tools.ToolsAndAgents import webTools, custom_tools

from Langgraph.chatbot_with_langgraph import State
from Langgraph.enhanced_chatbot_with_langgraph import llm_with_tools, tool_node


class Processing:

    def __init__(self):
        self.store = {}
        self.llm = ChatGroq(model=app_constants.LLM_MODEL, temperature=0.5, max_tokens=100)
        self.memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=5)

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
            print(f"Created new chat history for {session_id}")
        return self.store[session_id]

    def create_prompt(self, prompt_text):
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_text),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        return contextualize_q_prompt

    def initialize_custom_tools(self, db):
        return custom_tools(db)

    def initialize_web_tools(self):
        return webTools()

    def llm_tool_chain(self, llm):
        return Tool(
            name="LLM Search",
            func=llm.invoke,
            description="LLM basic chain"
        )

    class State(TypedDict):
        # Messages have the type "list". The `add_messages` function
        # in the annotation defines how this state key should be updated
        # (in this case, it appends messages to the list, rather than overwriting them)
        messages: Annotated[list, add_messages]

    def chatbot(self, state: State):
        print(f"All messages {state['messages']}")
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    def create_graph(self, db):
        # Initialize the LLM (Language Model)
        graph_builder = StateGraph(State)
        tools = [self.llm_tool_chain(self.llm)]

        self.llm.bind_tools(tools=tools)

        graph_builder.add_node("chatbot", self.chatbot)
        graph_builder.add_edge(START, "chatbot")

        graph_builder.add_node("tools", tool_node)

        graph_builder.add_conditional_edges("chatbot", tools_condition)

        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge("chatbot", END)

        # Compile graph builder
        graph = graph_builder.compile()

        # tools = []
        if db:
            retriever = db.as_retriever()
            tools.append(self.initialize_custom_tools(retriever))
        else:
            for t in self.initialize_web_tools():
                tools.append(t)
        # Initialize memory to store conversation history

        prompt = ChatPromptTemplate.from_messages(
            system_tool_prompt
        )
        # Create the agent (with the history-aware retriever and the prompt)
        agent = create_tool_calling_agent(self.llm, tools, prompt)

        # Return an agent executor with memory integration (this will execute the agent with history)
        agent_chain = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=self.memory,
            verbose=True,
            max_interations=2,
            handle_parsing_errors=str,
            early_stopping_method="force"
        )
        print(f"Tools -> {agent_chain.tools}")

        conversational_rag_chain = RunnableWithMessageHistory(
            agent_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="output"
        )

        return conversational_rag_chain

    def create_chain(self, db):
        model = ChatGroq(model=app_constants.LLM_MODEL, temperature=0.5, max_tokens=100)
        retriever = db.as_retriever()

        # Check on this
        history_aware_retriever = create_history_aware_retriever(model, retriever,
                                                                 self.create_prompt(contextualize_q_system_prompt))

        qa_prompt = self.create_prompt(system_prompt)

        question_answer_chain = create_stuff_documents_chain(model, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
        return conversational_rag_chain

import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_groq import ChatGroq

wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2000)

# Run query to outside world
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
print(f"Tool name is {wiki.name}")

axiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=2000)

# axiv
axiv = ArxivQueryRun(api_wrapper=axiv_wrapper)
print(f"Tool name is {axiv.name}")

# duck duck search
search = DuckDuckGoSearchRun(name="DuckDuckSearch", doc_content_chars_max=2000)

st.title("Langchain Search")

tools = [search, wiki, axiv]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, How can i help you today ?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is Generative AI ?"): st.session_state.messages.append(
    {"role": "user", "content": prompt})
st.chat_message("user").write(prompt)

## check this - AgentType.ZERO_SHOT_REACT_DESCRIPTION
llm = ChatGroq(model="Gemma2-9b-It",
               streaming=True)
search_agents = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                 handling_parse_errors=True)

with st.chat_message("assistant"):
    callbacks = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
    response = search_agents.run(st.session_state.messages, callbacks=[callbacks])
    st.session_state.messages.append({"role": "assistance", "content": response[1]})

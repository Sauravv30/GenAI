import os
import sqlite3
import streamlit as st
from langchain.agents import AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from sqlalchemy import create_engine

### Side panel ###
st.title(":blue[Cool] SqlChat :sunglasses:")
side = st.sidebar
side.title("Settings")
groq_api = side.text_input("Groq Token", type="password")
url = side.text_input("Database URL:")
db_name = side.text_input("Db:")
schema = side.text_input("Schema:")
username = side.text_input("Username: ")
password = side.text_input("Password: ", type="password")


def check_db():
    db = SQLDatabase.from_uri(database_uri=f"sqlite:///C:/Users/Saurav/Documents/sql/employee")
    resp = db.run("Select * FROM EMPLOYEE")
    print(resp)


os.environ["GROQ_API_KEY"] = ""
llm = ChatGroq(model="Gemma2-9b-It", streaming=True)


# @st.cache_resource(ttl="2h")
def configure_db(db_uri, user=None, password=None, db=None, db_type="LOCAL", schema=None):
    engine = None
    if db_type == "LOCAL":
        db_path = f"C:/Users/Saurav/Documents/sql/employee"
        # creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        # engine = create_engine(url=f"sqlite:///C:/Users/Saurav/Documents/sql/employee")
        engine = create_engine(url=db_uri)
    else:
        engine = create_engine(f"mysql+mysqldb://{user}:{password}@{db_uri}/{db}", schema=schema,
                               pool_recycle=3600, echo=True)
    return SQLDatabase(engine, sample_rows_in_table_info=10)


if "agent" not in st.session_state and url:
    db = configure_db(db_uri=url, user=username, password=password, db=db_name, schema=schema,
                      db_type="LOCAL")

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handling_parse_errors=True,
        max_iterations=3
    )
    st.session_state["agent"] = agent

# query = input("Type query")
# response = st.session_state["agent"].invoke({"input": query})
# print(response['output'])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I can help you to talk to your Database?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input(placeholder="List all Databases")
if prompt and url:
    # with st.chat_message("assistant"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner():
        callbacks = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = st.session_state["agent"].invoke(st.session_state.messages, callbacks=[callbacks],
                                                    handle_parsing_errors=True)
        st.session_state.messages.append(
            {"role": "assistant", "content": response['output']})
        st.chat_message("assistant").write(response['output'])

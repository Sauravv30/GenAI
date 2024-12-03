# Basically to keep the history of chat, we need to keep track over the session. Session is user specific, if session is available use the
# trim_messages: Helps to reduce how many messages we'are sending to the model.
# same create only when it is new chat
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# For trimmer
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
import os

# Message history class to wrap our model and make it stateful, This will keep track of inputs and outputs of model.
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# function for session history

sessions = {}


def session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in sessions:
        sessions[session_id] = ChatMessageHistory()
    return sessions[session_id]


config = {"configurable": {"session_id": "chat1"}}

groq_model = ChatGroq(model="Gemma2-9b-It")

with_message_history = RunnableWithMessageHistory(groq_model, session_history)
output = with_message_history.invoke(
    [
        HumanMessage(content="Hello, I am Saurav. I am a software engineer"),
        AIMessage(content="That's great, Saurav! It's nice to meet another software engineer. "),
        HumanMessage(content="What is my name and what do i do?")
    ], config

)

print(output.content)

# with_message_history = RunnableWithMessageHistory(groq_model, session_history)
#
output2 = with_message_history.invoke(
    [
        HumanMessage(content="What is my name and what do i do?")
    ], config=config,
)
print(output2.content)

config2 = {"configurable": {"session_id": "chat2"}}

output3 = with_message_history.invoke(
    [
        HumanMessage(content="What is my name and what do i do?")
    ], config=config2,
)
print(output3.content)

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant. Answer all the question to the best of your ability in {language} "),
     MessagesPlaceholder(variable_name="message")])

chain = prompt | groq_model

response = chain.invoke(
    {"message": [HumanMessage(content="Hi, Who is Shiva ?")], "language": "Hindi"}, config=config
)

print(response.content)

with_message_history_chain = RunnableWithMessageHistory(chain, session_history, input_messages_key="message")

config4 = {"configurable": {"session_id": "chat4"}}

result = with_message_history_chain.invoke(
    {"message": [HumanMessage(content="Hello I am Saurav")], "language": "hindi"}, config=config4

)
print(response.content)

## add trimmer to wipe of long history of chat and only consider last 100 tokens
trimmer = trim_messages(max_tokens=100, strategy="last", token_counter=groq_model, include_system=True,
                        allow_partial=False,
                        start_on="human")

chain_with_trimmer = RunnablePassthrough.assign(messages=itemgetter("message") | trimmer) | prompt | groq_model
with_message_history_chain_trimmer = RunnableWithMessageHistory(chain_with_trimmer, session_history,
                                                                input_messages_key="message")
result_trimmer = with_message_history_chain_trimmer.invoke(
    {"message": [HumanMessage(content="Hello I am Saurav")], "language": "hindi"}, config=config4

)
print(result_trimmer)
# chain.invoke({"message": [HumanMessage()]})

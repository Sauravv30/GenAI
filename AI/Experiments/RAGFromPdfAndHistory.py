# Document
# Vector Store
# Retrievers


import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_retrieval_chain
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
import bs4

# Message history class to wrap our model and make it stateful, This will keep track of inputs and outputs of model.
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# Loader
loader = WebBaseLoader(web_path="https://lilianweng.github.io/posts/2023-06-23-agent/", bs_kwargs=dict(
    parse_only=bs4.SoupStrainer(
        class_=("post-content", "post-title", "post-header")
    )
))
documents = loader.load()

# Chunks
character_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_doc = character_splitter.split_documents(documents)

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Vector DB
db = Chroma.from_documents(split_doc, embedding=embeddings)

retriever = db.as_retriever()
# print(retriever.batch(["TADDM", "Allocator"]))

# Model
model = ChatGroq(model="Llama3-8b-8192")

# Basic system prompt to tell the model what is to be done?
system_prompt = ("You are an assistant for question-answering tasks. "
                 "Use the following pieces of retrieved context to answer "
                 "the question. If you don't know the answer, say that you "
                 "don't know. Use three sentences maximum and keep the "
                 "answer concise."
                 "\n\n"
                 "{context}")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm=model, prompt=prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

response = rag_chain.invoke({"input": "What is Self-Reflection"})
print(response['answer'])

# Here adding the history with new user query

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

# prompt to the model that with new query also mention the chat history
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

history_aware_retriever = create_history_aware_retriever(model, retriever, contextualize_q_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

from langchain_core.messages import AIMessage, HumanMessage

chat_history = []
question = "What is Self-Reflection"
response1 = rag_chain.invoke({"input": question, "chat_history": chat_history})

chat_history.extend(
    [
        HumanMessage(content=question),
        AIMessage(content=response1["answer"])
    ]
)

question2 = "Tell me more about its ReAct?"
response2 = rag_chain.invoke({"input": question2, "chat_history": chat_history})
chat_history.extend(
    [
        HumanMessage(content=question2),
        AIMessage(content=response2["answer"])
    ]
)

print(response2['answer'])
print(chat_history)

## here we can add more session attached to keep the users deattached

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

response3 = rag_chain.invoke(
    {"input": "What is Task Decomposition?"},
    config={
        "configurable": {"session_id": "abc123"}
    },  # constructs a key "abc123" in `store`.
)["answer"]
print(response3)

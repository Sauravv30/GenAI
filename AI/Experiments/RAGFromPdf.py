# Document
# Vector Store
# Retrievers


import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# Message history class to wrap our model and make it stateful, This will keep track of inputs and outputs of model.
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# Loader
loader = PyPDFLoader(file_path=r"E:\Resume.pdf")
documents = loader.load()

# Chunks
character_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10, separator="/n")
split_doc = character_splitter.split_documents(documents)

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Vector DB
db = Chroma.from_documents(split_doc, embedding=embeddings, persist_directory='./rag_chroma_doc')
# Vector db objects is not runnable so it can't be part of chain
# db.asimilarity_search("")

# Retriever
# Here, is the way to make it runnable
retriever = db.as_retriever(
    search_type="similarity", search_kwargs={"k": 1}
)
# print(retriever.batch(["TADDM", "Allocator"]))


message = """
You are a helpful assistant. Answer all the question to the best of your ability from the given context only.
{question}

Context:
{context}
"""

# prompt
prompt = ChatPromptTemplate.from_messages(
    [("human", message)])

# parser = StrOutputParser

# Model
model = ChatGroq(model="Llama3-8b-8192")

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | model

while True:
    user_input = input("Enter your question here: ")
    if user_input == "End":
        break
    response = rag_chain.invoke(input=user_input)
    print(response.content)

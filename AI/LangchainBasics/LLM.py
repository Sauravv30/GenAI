import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain.llms import HuggingFaceHub
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA

load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
os.environ["PROJECT_NAME"] = os.getenv("PROJECT_NAME")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

llm = HuggingFaceHub(repo_id="HuggingFaceH4/zephyr-7b-beta",
                     model_kwargs={"temperature": 0.5, "max_length": 60, "max_new_tokens": 512})

template = ChatPromptTemplate([
    ("system",
     "You are an AI assistant the follows instructions extremely well. Please be truthful and give direct answers. If "
     "you do not know, say I am not prepared for this directly.")
])

# qa = RetrievalQA.from_chain_type(llm=llm, retriever=)

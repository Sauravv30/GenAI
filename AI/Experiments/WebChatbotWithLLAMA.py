import os

from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environments
load_dotenv()

# Set configurations for hugging face
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
os.environ["PROJECT_NAME"] = os.getenv("PROJECT_NAME")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"


# Data ingestion
def document_loader():
    loader = WebBaseLoader(web_path="https://medium.com/inside-machine-learning/what-is-a-transformer-d07dd1fbec04")
    return loader.load()


def document_splitting():
    document = document_loader()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    return splitter.split_documents(document)


def do_embeddings():
    split_document = document_splitting()
    hf_embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return split_document, hf_embedding


def store_in_chroma_db():
    document, embedding = do_embeddings()
    db = Chroma.from_documents(document, embedding, persist_directory="./chromaDb")
    # output = retriever.invoke("What is LSTM?")
    # print(output[0].page_content)
    return db.as_retriever()


def llm_call(llm, prompt):
    return llm(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']


def integrate_llm():
    llm = OllamaLLM(model="llama3.2")
    # output = llm("", max_length=50, num_return_sequences=1)
    retriever = store_in_chroma_db()
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the following question based only on the provided context.
        Think step by step before you answer the question.
        <context>
           {context} 
        </context>
        Question: {input}
        """

    )

    doc_chain = create_stuff_documents_chain(llm, prompt)
    # Retrieval chain
    retrival_chain = create_retrieval_chain(retriever, doc_chain)
    while True:
        user_input = input("->")
        if user_input == "end":
            break
        response = retrival_chain.invoke({"input": user_input})  # put question here
        print(response['answer'])


integrate_llm


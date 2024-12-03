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
import streamlit as st


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


# Load environments
@singleton
class ChatBot:

    def __init__(self):
        load_dotenv()
        # Set configurations for hugging face
        os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
        os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
        os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        self.retriever_chain = None

    # Data ingestion
    def document_loader(self, url):
        loader = WebBaseLoader(web_path=url)
        return loader.load()

    def document_splitting(self, document):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        return splitter.split_documents(document)

    def do_embeddings(self, split_document):
        hf_embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return split_document, hf_embedding

    def store_in_chroma_db(self, document, embedding):
        # document, embedding = do_embeddings()
        db = Chroma.from_documents(document, embedding, persist_directory="./chromaDb")
        # output = retriever.invoke("What is LSTM?")
        # print(output[0].page_content)
        return db.as_retriever()

    # def llm_call(llm, prompt):
    #     return llm(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']

    def integrate_llm(self, retriever):
        llm = OllamaLLM(model="llama3.2")
        # output = llm("", max_length=50, num_return_sequences=1)
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
        #Combine the input documents and create chain
        doc_chain = create_stuff_documents_chain(llm, prompt)
        # Retrieval chain

        chain = create_retrieval_chain(retriever, doc_chain)
        print(f"chain in {chain}")
        return chain

    def submit_request(self, url):
        content_splitting = self.document_splitting(self.document_loader(url))
        document, embedding = self.do_embeddings(content_splitting)
        retriever = self.store_in_chroma_db(document, embedding)
        self.retriever_chain = self.integrate_llm(retriever)
        return self.retriever_chain
        # print(f"Setting chain {self.retriever_chain}")

    def submit_question(self, user_question):
        print(f"Retriever {self.retriever_chain}")
        print(f"user question {user_question}")
        try:
            response = self.retriever_chain.invoke({"input": user_question})  # put question here
        except Exception as e:
            return e
        return response['answer']


class StreamExecution:

    retrival = "hello"
    def __init__(self):
        self.retrival ="hello"
        self.bot = ChatBot()
        self.url = ""
        self.question = ""

    def url_button_clicked(self):
        self.retrival = self.bot.submit_request(self.url)
        print(f"submit url -> {self.retrival}")

    def question_button_clicked(self):
        print(f"on click -> {self.retrival}")
        print(f"on click -> {self.question}")
        print(f"question bot {self.bot}")
        st.write(self.bot.submit_question(self.question))

    def start(self):
        st.title("Web Chatbot")

        self.url = st.text_input("Enter any blog url",
                                 value="https://medium.com/@gayani.parameswaran/advanced-q-a-chatbot-with-chain-and-retriever-using-langchain-7ad735b1d238")

        button = st.button("Send", on_click=self.url_button_clicked())
        self.url_button_clicked()
        print("count")
        self.question = st.text_input("Enter your question")
        st.button("Submit", on_click=self.question_button_clicked)


execution = StreamExecution()
execution.start()

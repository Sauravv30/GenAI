import logging
import os
from collections import deque

from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from Loaders import PdfLoader, WebLoader


# Load configurations from env file
def loadEnv():
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")


class CharService:

    # Constructor initialization
    def __init__(self):
        self.db = None
        self.documents = None
        self.logger = logging.getLogger(__name__)
        self.source = None
        self.session_name = None
        self.store = {}
        loadEnv()
        self.model = ChatGroq(model="Llama3-8b-8192", temperature=0.7, max_tokens=1000)

    # Method to load pdf
    def load_pdf(self, path):
        self.logger.info("Loading PDF document")
        documents = PdfLoader(path).load()
        self.logger.info("PDF loaded")
        self.documents = documents

    # Method to load web path
    def load_web(self, path):
        self.logger.info(f"Loading Web path {path}")
        documents = WebLoader(path=path,
                              # bs_kwargs=dict(
                              #     parse_only=bs4.SoupStrainer(
                              #         class_=("post-content", "post-title", "post-header")
                              #     )
                              # ),
                              ).load()
        self.logger.info("Web path loaded")
        self.documents = documents

    """
        Split_document method to split the input document into chunks
        CharacterTextSplitter - It is a simple character text splitter, using this splitter there is a chance to loose context, paragraphs
        RecursiveCharacterTextSplitter - Is a generic way to splitting the large document to smaller with context and paragraphs. recursive characters ["/n/n","/n"," ",""]    
    """

    def split_documents(self, document_type):
        self.logger.info(f"Self document {self.documents}")
        split_doc = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return split_doc.split_documents(self.documents)

    """
        apply_embeddings method to create embeddings of given document, for embedding HuggingFace open source model is used
        As we have multiple sources in input so we are deleting previous collection before creating new. 
    """

    def create_embeddings(self, documents):
        self.logger.info(f"Splitted documents {documents}")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        if self.db:
            self.db.delete_collection()
        self.db = Chroma.from_documents(documents, embeddings, persist_directory="./e2echatbot",
                                        collection_name="chatbot_context")

    """
        create_prompt - method is used to create prompts
        contextualize_q_prompt - is a prompt for model to generate the query where we are considering the latest question and previous chat history
    """

    def create_prompt(self):
        ## Prompt Template
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
        return contextualize_q_prompt



    """get_session_history method to store session id, it will create new session id when we do not have entry for 
    user otherwise it will return recent session id."""

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
            print(f"Created new chat history for {session_id}")
        return self.store[session_id]

    """
        create chain : method to create history aware chain
        system_prompt prompt to the model that it has to do with input
        conversational_rag_chain chain that will consider chat history and session id
        
        
    """

    def create_chain(self):

        # Check on this
        history_aware_retriever = create_history_aware_retriever(self.model, self.db.as_retriever(),
                                                                 self.create_prompt())

        system_prompt = (
            "You are helpful assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. Keep the answer accurate and best of your knowledge."
            "If you don't know the answer, say that you "
            "are Sorry about it and you have limited information from this context."
            "\n\n"
            "{context}"
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.model, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
        return conversational_rag_chain

    """
        start_chat_bot method to initialize the chat pre processing like loading data, chunking and embedding.
    """

    def start_chat_bot(self, source, path):
        self.source = source
        if source == 'PDF':
            self.load_pdf(path)
        elif source == 'WebUrl':
            self.load_web(path)
        documents = self.split_documents(source)
        self.create_embeddings(documents)

    """
        clear_context method to clear database.
    """

    def clear_context(self):
        if self.db:
            self.db.delete_collection()

    """
        invoke_user_request: method to take questions from user and invoke the chain for results
    """

    def invoke_user_request(self, question, session_name):
        print(f"session name {session_name}")
        # session_id = "session"
        history = self.get_session_history(session_id=session_name)
        print(f"History is {history}")
        response = self.create_chain().invoke({"input": question}, config={"configurable": {"session_id": session_name}})
        self.logger.info(f"Chat history {history}")
        return history.messages, response
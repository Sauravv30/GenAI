from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PreProcessing:
    def __init__(self):
        super().__init__()
        self.document_chunks = None
        self.db = None

    def do_chunking(self, documents):
        split_doc = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return split_doc.split_documents(documents)

    def do_embeddings(self, document_chunks):
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        # if self.db:
        #     self.db.delete_collection()
        self.db = Chroma.from_documents(document_chunks, embeddings, persist_directory="./chat_bot_db",
                                        collection_name="chatbot_context")
        return self.db.as_retriever()

    def do_preprocessing(self, documents):
        chunks = self.do_chunking(documents)
        return self.do_embeddings(chunks)

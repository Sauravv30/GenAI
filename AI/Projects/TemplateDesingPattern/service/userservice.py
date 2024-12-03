from Projects.TemplateDesingPattern.config.configuration import Configuration
from Projects.TemplateDesingPattern.loaders.loader import PDFLoader, WebLoader
from langchain_community.document_loaders import TextLoader
from Projects.TemplateDesingPattern.preprocessing.preprocessing import PreProcessing
from Projects.TemplateDesingPattern.processing.processing import Processing


class UserService:
    def __init__(self, processing, chain):
        Configuration(None).load()
        self.processing = processing
        self.chain = chain
        self.loader = None
        self.retriever = None

    def __init__(self):
        Configuration(None).load()
        self.processing = Processing()
        self.chain = self.processing.create_tools_chain(None)
        self.loader = None
        self.retriever = None

    # loading
    async def load_document_from_file(self, file_location, file_type):
        if file_type == "pdf":
            loader = PDFLoader(path=file_location).load()
        else:
            print(f"Loading content from text, {file_location}, {file_type}")
            loader = TextLoader(file_path=file_location).load()
        self.create_and_save_embeddings(loader)

    async def load_document_from_web(self, url):
        loader = WebLoader(path=url).load()
        self.create_and_save_embeddings(loader)

    async def load_document_from_else(self, url):
        pass

    def create_and_save_embeddings(self, loader):
        print("Creating service................")

        # documents = PDFLoader(path=f"../uploaded_pdfs/Resume.pdf").load()
        self.retriever = PreProcessing().do_preprocessing(loader)
        # Processing

        # service = UserService(processing, chain)

    # storage

    def invoke_user_request(self, question, session_name):
        self.chain = self.processing.create_tools_chain(self.retriever)
        print(f"session name {session_name}")
        # session_id = "session"
        history = self.processing.get_session_history(session_id=session_name)
        print(f"User asked --> {question}")
        response = self.chain.invoke({"input": question},
                                     config={"configurable": {"session_id": session_name}})
        # self.logger.info(f"Chat history {history}")
        return response['output'].strip()

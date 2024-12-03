from typing import Optional, Dict, Any

from langchain.document_loaders import PyPDFLoader, WebBaseLoader


# Loader base class
class Loader:
    def __init__(self, path):
        self.path = path

    def load(self):
        # Default load method can be implemented here if required
        pass


# PDF Loader
class PdfLoader(Loader):
    def __init__(self, path):
        super().__init__(path)
        self.loader = PyPDFLoader(file_path=path, extract_images=False)  # Ensure PyPDFLoader is imported or defined

    def load(self):
        return self.loader.load()


# Web Loader
class WebLoader(Loader):
    def __init__(self, path, bs_kwargs: Optional[Dict[str, Any]] = None):  # Unified parameter name for path
        super().__init__(path)  # Path is consistent with the parent class
        self.loader = WebBaseLoader(web_path=path, bs_kwargs=bs_kwargs)  # Ensure WebBaseLoader is imported or defined

    def load(self):
        return self.loader.load()  # Assuming WebBaseLoader has a load() method

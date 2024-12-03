from typing import Optional, Dict, Any

from template.template import BaseLoaders
from langchain_community.document_loaders import WebBaseLoader,PyPDFLoader, TextLoader


class PDFLoader(BaseLoaders):
    def __init__(self, path):
        super().__init__(self)
        self.loader = PyPDFLoader(file_path=path, extract_images=False)

    def load(self):
        return super().load()


class WebLoader(BaseLoaders):
    def __init__(self, path, bs_kwargs: Optional[Dict[str, Any]] = None):
        # Unified parameter name for path
        super().__init__(self)  # Path is consistent with the parent class
        self.loader = WebBaseLoader(web_path=path, bs_kwargs=bs_kwargs, raise_for_status=True)  # Ensure WebBaseLoader is imported or defined

    def load(self):
        return self.loader.load()  # Assuming WebBaseLoader has a load() method


class TextBaseLoader(BaseLoaders):
    def __init__(self, path):
        # Unified parameter name for path
        super().__init__(self)  # Path is consistent with the parent class
        self.loader = TextLoader(file_path=path)  # Ensure WebBaseLoader is imported or defined

    def load(self):
        return self.loader.load()  # Assuming WebBaseLoader has a load() method

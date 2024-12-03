import os

from template.template import BaseConfig
from dotenv import load_dotenv


class Configuration(BaseConfig):
    def __init__(self, path):
        super().__init__(path)

    def load(self):
        load_dotenv()
        os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
        os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# template for backend modules
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(messages)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class BaseConfig:

    def __init__(self, path):
        self.path = path

    @abstractmethod
    def load(self):
        pass


class BaseLoaders:
    def __init__(self, loader):
        self.loader = loader

    @abstractmethod
    def load(self):
        return self.loader.load()


class BaseService:
    def __init__(self):
        pass

    @abstractmethod
    def log_info(self, message):
        logger.info(message)

    @abstractmethod
    def log_debug(self, message):
        logger.debug(message)

    @abstractmethod
    def log_error(self, message):
        logger.error(message)


class BasePreprocessing:
    def __init__(self):
        pass

    def do_chunking(self, documents):
        pass

    def do_embeddings(self, chunks):
        pass

    def do_preprocessing(self, documents):
        pass


class Vectorization:
    def __init__(self):
        pass

    def do_vectorization(self):
        pass


class Prompting:
    def __init__(self):
        pass


class Chaining:
    def __init__(self):
        pass

    def create_chain(self):
        pass


class UserRequest:
    def __init__(self):
        pass

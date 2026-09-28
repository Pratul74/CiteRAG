from abc import abstractmethod, ABC
from langchain_core.documents import Document

class BaseSplitter(ABC):

    @abstractmethod
    def split(self, docs: list[Document]) -> list[Document]:
        pass

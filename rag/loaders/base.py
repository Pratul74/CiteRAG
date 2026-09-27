from abc import abstractmethod, ABC
from .document import Document

class BaseLoader(ABC):
    @abstractmethod
    def load(self, source:any) -> Document:
        pass



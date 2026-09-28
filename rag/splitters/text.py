from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from .base import BaseSplitter

class TextSplitter(BaseSplitter):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        self._char_splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split(self, docs: list[Document]) -> list[Document]:
        return self._char_splitter.split_documents(docs)
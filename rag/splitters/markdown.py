from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from .base import BaseSplitter

class MarkdownSplitter(BaseSplitter):
    _HEADERS_TO_SPLIT_ON = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    def __init__(self, chunk_size: int=1000, chunk_overlap:int=150):
        self._header_splitter=MarkdownHeaderTextSplitter(self._HEADERS_TO_SPLIT_ON)
        self._char_splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def split(self, docs: list[Document]) -> list[Document]:
        final=[]
        for doc in docs:
            header_chunks=self._header_splitter.split_text(doc.page_content)
            for chunk in header_chunks:
                chunk.metadata.update(doc.metadata)
            final.extend(self._char_splitter.split_documents(header_chunks))
        return final
        



        



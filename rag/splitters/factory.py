from .base import BaseSplitter
from .url import UrlSplitter
from .pdf import PDFSplitter
from .text import TextSplitter
from .markdown import MarkdownSplitter

class SplitterFactory:
    _REGISTRY : dict[str, type[BaseSplitter]] ={
        "markdown": MarkdownSplitter,
        "url": UrlSplitter,
        "pdf": PDFSplitter,
        "text": TextSplitter
    }

    @classmethod
    def get_splitter(cls, source_type: str, **kwargs) -> BaseSplitter:
        try:
            splitter_cls=cls._REGISTRY
        except KeyError:
            raise ValueError(
                f"No splitter registered for source_type={source_type!r}. "
                f"Available: {list(cls._REGISTRY)}"
            )
        return splitter_cls(**kwargs)
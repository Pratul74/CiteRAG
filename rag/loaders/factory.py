import mimetypes
from .pdf import PDFLoader
from .text import TextLoader
from .markdown import MarkdownLoader
from pathlib import Path
from .document import Document
from .exceptions import LoaderError
from .url import UrlLoader



class LoaderFactory:
    _EXTENSION_MAP={
        ".pdf": PDFLoader,
        ".txt": TextLoader,
        ".markdown": MarkdownLoader,
        ".md": MarkdownLoader
    }

    @classmethod
    def load_file(cls, path: str | Path, filename: str | None = None) -> Document:
        name=filename or Path(path).name
        ext=Path(name).suffix.lower()
        load_cls=cls._EXTENSION_MAP.get(ext)
        if not load_cls:
            mime, _ = mimetypes.guess_type(name)
            if mime == "application/pdf":
                load_cls=PDFLoader
            elif mime and mime.startswith("text/"):
                load_cls=TextLoader
            else:
                raise LoaderError(
                    f"Unsupported file type: {name} ({mime})"
                )
        return load_cls().load(path)

    @classmethod
    def load_url(cls, url: str) -> Document:
        return UrlLoader().load(url)

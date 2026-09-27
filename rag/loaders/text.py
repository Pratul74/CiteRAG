import chardet
from .document import Document
from .base import BaseLoader
from .exceptions import LoaderError
from pathlib import Path
from utils import hash_id

class TextLoader(BaseLoader):
    def load(self, source: str | Path | bytes) -> Document:
        if isinstance(source, (str, Path)) and Path(source).exists():
            raw_bytes=Path(source).read_bytes()
            filename=Path(source).name
        elif isinstance(source, bytes):
            raw_bytes=source
            filename="uploaded.txt"
        else:
            raw_bytes=source.encode(encoding="utf-8")
            filename="inline.txt"
        detected=chardet.detect(raw_bytes)
        encoding=detected.get('encoding') or "utf-8"
        text=raw_bytes.decode(encoding, errors="replace")

        if not text.strip():
            raise LoaderError(f"Empty text file: {filename}")
        return Document(
            source_id=hash_id(raw_bytes),
            source_type="txt",
            title=filename,
            raw_text=text,
            meta_data={
                "filename": filename,
                "detected_encoding": encoding
            }
        )



        
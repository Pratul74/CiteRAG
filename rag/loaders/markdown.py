from .base import BaseLoader
from .exceptions import LoaderError
from .document import Document
from markdown_it import MarkdownIt
from pathlib import Path
from utils import hash_id

class MarkdownLoader(BaseLoader):
    def load(self, source: str | Path | bytes) -> Document:
        text, filename = self._read(source)
        md = MarkdownIt()
        tokens = md.parse(text)

        headings=[]
        for i, t in enumerate(tokens):
            if t.type == "inline" and i>0 and tokens[i-1].tag in ("h1", "h2", "h3"):
                headings.append(t.content)

        if not text.strip():
            raise LoaderError(f"Empty markdown file: {filename}")

        return Document(
            source_id=hash_id(text),
            source_type="markdown",
            title=headings[0] if headings else filename,
            raw_text=text,
            meta_data={"filename": filename, "headings": headings},
        )

    @staticmethod
    def _read(source: str | Path | bytes) -> tuple[str, str]:
        if isinstance(source, (str, Path)) and Path(source).exists():
            path = Path(source)
            return path.read_text(encoding="utf-8", errors="replace"), path.name
        if isinstance(source, bytes):
            return source.decode("utf-8", errors="replace"), "uploaded.md"
        return str(source), "inline.md"

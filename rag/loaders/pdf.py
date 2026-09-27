from pathlib import Path

import pymupdf
import pytesseract

from .base import BaseLoader
from .document import Document
from .exceptions import LoaderError
from utils import hash_id


class PDFLoader(BaseLoader):

    MIN_CHAR_LEN = 20

    def load(self, source: str | Path | bytes) -> Document:

        if isinstance(source, (str, Path)):
            raw_bytes = Path(source).read_bytes()
            filename = Path(source).name
        else:
            raw_bytes = source
            filename = "uploaded.pdf"

        with pymupdf.open(stream=raw_bytes, filetype="pdf") as doc:

            pages_text = []
            ocr_pages = []

            for page_no, page in enumerate(doc):

                text = page.get_text("text").strip()

                if len(text)<self.MIN_CHAR_LEN:
                    text=self._ocr_page(page)
                    ocr_pages.append(page_no)

                pages_text.append(text)

        final_text="\n\n".join(pages_text)

        if not final_text.strip():
            raise LoaderError(f"Text not found in {filename}")

        return Document(
            source_id=hash_id(raw_bytes),
            source_type="pdf",
            title=filename,
            raw_text=final_text,
            meta_data={
                "filename": filename,
                "page_count": len(pages_text),
                "ocr_pages": ocr_pages,
            },
        )

    def _ocr_page(self, page: pymupdf.Page) -> str:

        pix = page.get_pixmap(dpi=300)

        image = pix.pil_image()

        return pytesseract.image_to_string(image)
        

        

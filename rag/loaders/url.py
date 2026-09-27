from .base import BaseLoader
from .exceptions import LoaderError
from .document import Document
from utils import hash_id
import httpx
from httpx import HTTPError
import trafilatura
from datetime import datetime, timezone
import re


class UrlLoader(BaseLoader):
    @staticmethod
    def _clean_markdown(text: str) -> str:

        text = re.sub(r"\[\d+(?:,\s*\d+)*\]", "", text)

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
    
    def load(self, source: str) -> Document:
        url=source.strip()
        try:
            headers = {
                "User-Agent": (
                    "CiteRAG/1.0 "
                    "(https://github.com/Pratul74/CiteRAG; "
                    "pratulkumar74@gmail.com)"
                )
            }
            resp=httpx.get(
                url=url,
                timeout=15,
                follow_redirects=True,
                headers=headers,
            )
            resp.raise_for_status()
        except HTTPError as e:
            raise LoaderError(f"Failed to fetch url: {url}") from e
        extracted=trafilatura.bare_extraction(
            filecontent=resp.text,
            include_comments=False,
            include_tables=True,
            output_format="markdown",
        )
        if extracted is None or not extracted.raw_text or len(extracted.raw_text.strip())<50:
            raise LoaderError(
                f"Could not extract meaningful content from {url}. "
                "Page may be JS-rendered — consider a Playwright-based fetch fallback."
            )
        title=(extracted.title if extracted.title else None) or url
        return Document(
            source_id=hash_id(url),
            source_type="url",
            title=title,
            raw_text=self._clean_markdown(extracted.raw_text),
            meta_data={
                "url": url,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "status_code": resp.status_code,
            },
        )









            
        
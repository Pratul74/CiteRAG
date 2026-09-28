from langchain_core.documents import Document

def to_langchain_document(docs) -> Document:
    if not isinstance(docs, list):
        docs=[docs]
    return [
        Document(
            page_content=doc.raw_text,
            metadata={**doc.meta_data, "source_id": doc.source_id, "source_type": doc.source_type, "title": doc.title}
        )
        for doc in docs
    ]
from dataclasses import dataclass, field

@dataclass
class Document:
    source_id:str
    source_type:str
    title:str
    raw_text:str
    meta_data:dict[str, any] = field(default_factory=dict)

    @property
    def is_empty(self) -> bool:
        return not self.raw_text or not self.raw_text.strip()


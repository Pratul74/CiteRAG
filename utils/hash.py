import hashlib

def hash_id(payload: bytes | str) -> str:
    if isinstance(payload, str):
        payload=payload.encode(encoding="utf-8", errors="ignore")
    return hashlib.sha256(payload).hexdigest()[:16]
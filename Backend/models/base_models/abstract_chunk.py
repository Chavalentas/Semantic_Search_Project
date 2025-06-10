from pydantic import BaseModel


class AbstractChunk(BaseModel):
    """Represents a chunk (piece of text information) taken from the abstract.
    Args:
        BaseModel (_type_): The base model used by pydantic.
    """
    paperId: str
    chunkText: str

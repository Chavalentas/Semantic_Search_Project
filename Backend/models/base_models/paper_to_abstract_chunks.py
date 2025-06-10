from pydantic import BaseModel
from models.base_models import paper, abstract_chunk


class PaperToAbstractChunks(BaseModel):
    """Represents a class that maps a paper to its abstract chunks.
    Args:
        BaseModel (_type_): The base model used by pydantic.
    """
    paper: paper.Paper
    chunks: list[abstract_chunk.AbstractChunk]

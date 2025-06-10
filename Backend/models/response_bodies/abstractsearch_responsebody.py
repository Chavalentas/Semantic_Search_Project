from pydantic import BaseModel
from models.base_models import paper_to_abstract_chunks


class AbstractSearchResponseBody(BaseModel):
    """Represents a HTTP response body that contains results from the semantic search in the paper's abstract.
    Args:
        BaseModel (_type_): The base model used by pydantic.
    """

    result: list[paper_to_abstract_chunks.PaperToAbstractChunks]

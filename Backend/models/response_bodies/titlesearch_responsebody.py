from pydantic import BaseModel
from models.base_models import paper


class TitleSearchResponseBody(BaseModel):
    """Represents a HTTP response body that contains results from the semantic search in the paper's title.
    Args:
        BaseModel (_type_): The base model used by pydantic.
    """

    result: list[paper.Paper]

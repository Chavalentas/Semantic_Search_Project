from pydantic import BaseModel
from models.base_models import paper


class TitleSearchLexResponseBody(BaseModel):
    """Represents a HTTP response body that contains results from the lexical search in the paper's title.
    Args:
        BaseModel (_type_): The base model used by pydantic.
    """

    result: list[paper.Paper]

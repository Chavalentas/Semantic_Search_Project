from pydantic import BaseModel


class AbstractSearchRequestBody(BaseModel):
    """Represents a HTTP request body that can be used to trigger semantic search in the paper's abstract.
    Args:
        BaseModel (_type_): The base model used by pydantic.
    """

    query: str
    amount: int

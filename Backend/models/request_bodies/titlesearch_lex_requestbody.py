from pydantic import BaseModel


class TitleSearchLexRequestBody(BaseModel):
    """Represents a HTTP request body that can be used to trigger lexical search in the paper's title.
    Args:
        BaseModel (_type_): The base model used by pydantic.
    """

    query: str
    amount: int

from pydantic import BaseModel
from models.base_models.author import Author


class Paper(BaseModel):
    """Represents a paper consisting of title, abstract, publication date and its authors.
    Args:
        BaseModel (_type_): The base model used by pydantic.
    """
    paperId: str
    title: str
    abstract: str
    publicationDate: str
    authors: list[Author]

from pydantic import BaseModel


class Author(BaseModel):
    """Represents an author of the paper (full name contains the first and last name of the author).
    Args:
        BaseModel (_type_): The base model used by pydantic.
    """
    fullName: str

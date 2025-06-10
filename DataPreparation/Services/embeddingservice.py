from abc import ABC, abstractmethod

class EmbeddingService(ABC):
    """Represents an abstract embedding service.

    Args:
        ABC (_type_): The abstract base class.
    """
    @abstractmethod
    def create_embedding(self, text: str) -> list[float]:
        """Creates an embedding for the given text.

        Args:
            text (str): The text to embed.

        Returns:
            list[float]: The resulting embedding vector.
        """
        pass
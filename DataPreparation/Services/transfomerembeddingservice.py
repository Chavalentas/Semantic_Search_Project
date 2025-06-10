from sentence_transformers import SentenceTransformer
from Services.embeddingservice import EmbeddingService
from Services.helper import Helper

class TransformerEmbeddingService(EmbeddingService):
    """Represents an embedding service that uses sentence transformers
    to embed data (neural network model designed to generate dense vector representations for sentences).

    Args:
        EmbeddingService (_type_): The base embedding service. 
    """
    def __init__(self, embedder: SentenceTransformer):
        """Initializes a new instance of TransformerEmbeddingService.

        Args:
            embedder (SentenceTransformer): The sentence transformer.
        """
        Helper.ensure_instance(embedder, SentenceTransformer, "embedder must be of type SentenceTransformer!")
        self.embedder = embedder

    def create_embedding(self, text: str) -> list[float]:
        """Creates an embedding for the given text using a sentence transformer.

        Args:
            text (str): The text to embed.

        Returns:
            list[float]: The resulting embedding vector.
        """
        Helper.ensure_type(text, str, "text must be a str!")

        if type(text) != str:
            raise TypeError("text must be a str!")
    
        text_embedding = [float(el) for el in list(self.embedder.encode(text))]
        return text_embedding
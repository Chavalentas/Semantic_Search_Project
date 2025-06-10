from models.abstract_chunk import AbstractChunk
from models.paper import Paper
from models.helper import Helper

class PaperToAbstractChunks:
    """Represents a class matching paper to abstract chunks.
    """
    def __init__(self, paper: Paper, chunks: list[AbstractChunk]):
        """Initializes a new instance of PaperToAbstractChunks.

        Args:
            paper (Paper): The paper.
            chunks (list[AbstractChunk]): The abstract chunks belonging to the paper.
        """
        self.__chunks = []
        self.set_paper(paper)
        self.set_chunks(chunks)

    def get_paper(self) -> Paper:
        """Returns the paper.

        Returns:
            Paper: The paper.
        """
        return self.__paper
    
    def set_paper(self, paper: Paper):
        """Sets the paper.

        Args:
            paper (Paper): The paper.
        """
        Helper.ensure_instance(paper, Paper, "paper must be of type Paper!")
        self.__paper = paper

    def get_chunks(self) -> list[AbstractChunk]:
        """Returns the abstract chunks belonging to the paper.

        Returns:
            list[AbstractChunk]: The list of abstract chunks.
        """
        return self.__chunks
    
    def set_chunks(self, chunks: list[AbstractChunk]):
        """Sets the abstract chunks belonging to the paper.

        Args:
            chunks (list[AbstractChunk]): The abstract chunks belonging to the paper. 
        """
        Helper.ensure_list_of_instance(chunks, AbstractChunk, "chunks must be a list!", "chunks must contain only instance of AbstractChunk!")
        self.__chunks = chunks
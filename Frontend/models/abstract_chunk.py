from models.helper import Helper

class AbstractChunk:
    """Represents a piece of information from abstract.
    """
    def __init__(self, paper_id: str, text: str):
        """Initializes a new instance of AbstractChunk.

        Args:
            paper_id (str): The paper ID.
            text (str): The text of the abstract chunk.
        """
        self.__paper_id = ""
        self.__text = ""
        self.set_paper_id(paper_id)
        self.set_text(text)

    def get_paper_id(self) -> str:
        """Returns the paper ID.

        Returns:
            str: The paper ID.
        """
        return self.__paper_id

    def set_paper_id(self, paper_id: str):
        """Sets the ID of the paper.

        Args:
            paper_id (str): The paper ID.
        """
        Helper.ensure_type(paper_id, str, "paper_id must be an str!")

        self.__paper_id = paper_id 

    def get_text(self) -> str:
        """Returns the text of the abstract chunk.

        Returns:
            str: The text of the abstract chunk.
        """
        return self.__text

    def set_text(self, text: str):
        """Sets the text of the abstract chunk.

        Args:
            text (str): The text of the abstract chunk.

        Raises:
            ValueError: Is thrown if the lenght of the abstract chunk is 0.
        """
        Helper.ensure_type(text, str, "text must be a string!")
        
        if len(text) == 0:
            raise ValueError("text cannot be empty!")

        self.__text = text 
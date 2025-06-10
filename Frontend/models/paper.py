from models.author import Author
from models.helper import Helper

class Paper:
    """Represents a paper.
    """
    def __init__(self, paper_id: int, title: str, abstract: str, date_time: str, authors: list[Author]):
        """Initializes a new instance of Paper.

        Args:
            paper_id (int): The paper ID.
            title (str): The paper title.
            abstract (str): The paper abstract.
            date_time (str): The date of publication.
            authors (list[Author]): The paper authors.
        """
        self.__paper_id = ""
        self.__title = ""
        self.__abstract = ""
        self.__date_time = ""
        self.__authors = []
        self.set_id(paper_id)
        self.set_title(title)
        self.set_abstract(abstract)
        self.set_datetime(date_time)
        self.set_authors(authors)

    def get_id(self) -> str:
        """Returns the paper ID.

        Returns:
            str: The paper ID.
        """
        return self.__paper_id

    def set_id(self, paper_id: str):
        """Sets the paper ID.

        Args:
            paper_id (str): The paper ID.
        """
        Helper.ensure_type(paper_id, str, "paper_id must be a str!")

        self.__paper_id = paper_id 

    def get_title(self) -> str:
        """Returns the title of the paper.

        Returns:
            str: The paper title.
        """
        return self.__title

    def set_title(self, title: str):
        """Sets the paper title.

        Args:
            title (str): The title of the paper.

        Raises:
            ValueError: Is thrown if the length of the title is 0.
        """
        Helper.ensure_type(title, str, "title must be a string!")
        
        if len(title) == 0:
            raise ValueError("title cannot be empty!")

        self.__title = title 

    def get_abstract(self) -> str:
        """Returns the abstract.

        Returns:
            str: The abstract text.
        """
        return self.__abstract

    def set_abstract(self, abstract: str):
        """Sets the abstract text.

        Args:
            abstract (str): The abstract text.

        Raises:
            ValueError: Is thrown if the length of the abstract is 0.
        """
        Helper.ensure_type(abstract, str, "abstract must be a string!")
        
        if len(abstract) == 0:
            raise ValueError("abstract cannot be empty!")

        self.__abstract = abstract 

    def get_datetime(self) -> str:
        """Returns the publication date of the paper.

        Returns:
            str: The publication date of the paper.
        """
        return self.__date_time

    def set_datetime(self, date_time: str):
        """Sets the publication date of the paper.

        Args:
            date_time (str): The publication date of the paper.

        Raises:
            ValueError: Is thrown if the length of the publication date is 0.
        """
        Helper.ensure_type(date_time, str, "date_time must be a string!")
        
        if len(date_time) == 0:
            raise ValueError("date_time cannot be empty!")

        self.__date_time = date_time 

    def get_authors(self) -> list[Author]:
        """Returns the authors of the paper.

        Returns:
            list[Author]: The authors of the paper.
        """
        return self.__authors
    
    def set_authors(self, authors: list[Author]):
        """Sets the authors of the paper.

        Args:
            authors (list): The list of authors.
        """
        Helper.ensure_type(authors, list, "authors must be a list!")

        for el in authors:
            Helper.ensure_instance(el, Author, "authors must contain objects of type Author!")

        self.__authors = authors
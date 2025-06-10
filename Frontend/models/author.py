from models.helper import Helper

class Author:
    """Represents the information about the author.
    """
    def __init__(self, full_name: str):
        """Initializes a new instance of Author.

        Args:
            full_name (str): The full name of the author.
        """
        self.__full_name = ""
        self.set_full_name(full_name)

    def get_full_name(self) -> str:
        """Returns the full name of the author.

        Returns:
            str: The full name of the author.
        """
        return self.__full_name

    def set_full_name(self, full_name: str):
        """Sets the full name of the author.

        Args:
            full_name (str): The full name of the author.

        Raises:
            ValueError: Is thrown if the length of the author name is 0.
        """
        Helper.ensure_type(full_name, str, "full_name must be a string!")
        
        if len(full_name) == 0:
            raise ValueError("full_name cannot be empty!")

        self.__full_name = full_name 
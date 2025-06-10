from abc import ABC, abstractmethod

class APIHandler(ABC):
    """Represents an abstract API handler.

    Args:
        ABC (_type_): The abstract base class.
    """
    @abstractmethod
    def fetch_data(self, url: str) -> dict:
        """Represents an abstract method
        that fetches data from the given URL.

        Args:
            url (str): The URL to fetch the data from.

        Returns:
            dict: The response as a dictionary.
        """
        pass
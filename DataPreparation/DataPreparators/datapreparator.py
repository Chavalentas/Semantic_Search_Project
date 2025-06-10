from abc import ABC, abstractmethod

class DataPreparator(ABC):
    """Represents an abstract data preparator.

    Args:
        ABC (_type_): The abstract base class.
    """
    @abstractmethod
    def prepare_data(self, data_dict: dict) -> dict:
        """Prepares the data represented as a dictionary.

        Args:
            data_dict (dict): The data to prepare.

        Returns:
            dict: The result of data preparation.
        """
        pass
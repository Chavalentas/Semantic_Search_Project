from abc import ABC, abstractmethod

class PreprocessingService(ABC):
    """Performs abstract preprocessing.

    Args:
        ABC (_type_): The abstract base class.
    """
    @abstractmethod
    def preprocess(self, data: str) -> str:
        """Preprocesses the data passed as a text string.

        Args:
            data (str): The data to preprocess.

        Returns:
            str: The preprocessed data.
        """
        pass
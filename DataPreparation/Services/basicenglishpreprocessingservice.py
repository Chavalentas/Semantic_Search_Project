from Services.preprocessingservice import PreprocessingService
from Services.helper import Helper
import re

class BasicEnglishPreprocessingService(PreprocessingService):
    """Performs basic preprocessing for the English language.

    Args:
        PreprocessingService (_type_): The abstract preprocessing service.
    """
    def __init__(self, stopwords: list[str]):
        """Initializes a new instance of BasicEnglishPreprocessingService.

        Args:
            stopwords (list[str]): A list of stopwords to exclude.
        """
        Helper.ensure_list_of_type(stopwords, str, "stopwords must be a list!", "stopwords must contain elements of type string!")
        self.stopwords = list(set([el.lower() for el in stopwords]))
        
    def preprocess(self, data: str) -> str:
        """Preprocesses the data passed as a text string.
        Applies lowercasing and removal of stopwords.
        Args:
            data (str): The data to preprocess.

        Returns:
            str: The preprocessed data.
        """
        Helper.ensure_type(data, str, "data must be a str!")
        lowercased = data.lower()
        word_tokens = re.findall(r'\d+|\w+', lowercased)
        word_tokens = [el for el in word_tokens if el not in self.stopwords]
        result = ' '.join(word_tokens)
        return result
        
        
import datetime
from DataPreparators.datapreparator import DataPreparator
import copy
from Services.helper import Helper

class ArxivDataPreparator(DataPreparator):
    """Represents a data preparator the prepare data fetched from the arXiv API.

    Args:
        DataPreparator (_type_): The abstract data preparator.
    """
    def __init__(self, amount_to_extract: int, exclude_empty_titles: bool, exclude_empty_abstracts: bool):
        """Initializes a new instance of ArxivDataPreparator.

        Args:
            amount_to_extract (int): The amount of papers to extract from the API result.
            exclude_empty_titles (bool): A boolean indicating whether empty titles should be excluded.
            exclude_empty_abstracts (bool): A boolean indicating whether empty abstracts should be excluded.
        """
        self.__set_amount_to_extract(amount_to_extract)
        self.__set_exclude_empty_titles(exclude_empty_titles)
        self.__set_exclude_empty_abstracts(exclude_empty_abstracts)

    def prepare_data(self, data_dict: dict) -> dict:
        """Prepares the data represented as a dictionary.

        Args:
            data_dict (dict): The data to prepare.

        Returns:
            dict: The result of data preparation.
            Format: {"arxivPapers": [
               {"id": <paper-id>, "publicationDate": <publication-date>, "title": <paper-title>, "abstract": <paper-abstract>,
                 "authors": [{"fullName": <author-name>}, ...]},
                 ...
            ]}
        """
        Helper.ensure_type(data_dict, dict, "data_dict must be a dict!")
        
        data_dict_c = copy.deepcopy(data_dict)
        result_list = data_dict_c["arxivPapers"]

        if self.__exclude_empty_titles:
            result_list = [el for el in result_list if el["title"] is not None]

        if self.__exclude_empty_abstracts:
            result_list = [el for el in result_list if el["abstract"] is not None]

        result_list = self.__remove_duplicate_ids(result_list)

        for el in result_list:
            if el["publicationDate"] is None:
                continue
            dt = datetime.datetime.strptime(el["publicationDate"], "%Y-%m-%dT%H:%M:%SZ")
            dt = datetime.datetime(dt.year, dt.month, dt.day)
            el["publicationDate"] = dt

        data_dict_c["arxivPapers"] = result_list[:self.__amount_to_extract]
        return data_dict_c
    
    def __remove_duplicate_ids(self, papers: list):
        """Removes duplicate papers by ID.

        Args:
            papers (list[dict]): List of paper dictionaries.

        Returns:
            list[dict]: The result list of dictionaries.
        """
        Helper.ensure_type(papers, list, "papers must be a list!")

        result = []
        ids = []

        for el in papers:
            if el["id"] in ids:
                continue
            ids.append(el["id"])
            result.append(el)
        return result

     
    def __set_amount_to_extract(self, amount_to_extract: int):
        """Sets the amount of papers to extract from the API result.

        Args:
            amount_to_extract (int): The amount of papers to extract.

        Raises:
            ValueError: Is thrown if the amount of papers to extract
            is equal or less than 0.
        """
        Helper.ensure_type(amount_to_extract, int, "amount_to_extract must be an int!")
        
        if amount_to_extract <= 0:
            raise ValueError("amount_to_extract must be greater than 0!")
        
        self.__amount_to_extract = amount_to_extract

    def __set_exclude_empty_titles(self, exclude_empty_titles: bool):
        """Sets a boolean indicating whether empty titles should be excluded.

        Args:
            exclude_empty_titles (bool): A boolean indicating whether 
            empty titles should be excluded.
        """
        Helper.ensure_type(exclude_empty_titles, bool, "exclude_empty_titles must be an bool!")
        
        self.__exclude_empty_titles = exclude_empty_titles

    def __set_exclude_empty_abstracts(self, exclude_empty_abstracts: bool):
        """Sets a boolean indicating whether empty abstracts should be excluded.

        Args:
            exclude_empty_abstracts (bool): A boolean indicating whether 
            empty abstracts should be excluded.
        """
        Helper.ensure_type(exclude_empty_abstracts, bool, "exclude_empty_abstracts must be an bool!")
        
        self.__exclude_empty_abstracts = exclude_empty_abstracts
import requests
import json
from models.author import Author
from config import Config
from models.paper import Paper
from models.helper import Helper

class TitleSearchService:
    """A service containing functions to communicate with server to retrieve information about paper titles.
    """
    def __init__(self):
        """Initializes a new instance of TitleSearchService.
        """
        self.__config = Config()

    def search_by_title(self, query: str, amount: int) -> list[Paper]:
        """Creates a HTTP request to search for titles using semantic search.

        Args:
            query (str): The query.
            amount (int): The amount of matches to return.

        Raises:
            ValueError: Is thrown if the length of the query is 0.
            ValueError: Is thrown if the amount of matches is negative.

        Returns:
            list[Paper]:  The matches (list of corresponding papers).
        """
        Helper.ensure_type(query, str, "query must be a string!")
        Helper.ensure_type(amount, int, "amount must be an int!")

        if len(query) == 0:
            raise ValueError("query cannot be empty!")
        
        if amount < 0:
            raise ValueError("amount cannot be negative!")
        
        try:
            request_body = json.dumps({"query": query, "amount": amount})
            headers = {"Content-Type": "application/json"}
            response = requests.post(self.__config.backend_url + "/title/search", data=request_body, headers=headers)
            response_json = response.json()
            result = self.__parse_search_by_title_result_list(response_json["result"])
            return result
        except Exception as e:
            raise

    def search_by_title_lexical(self, query: str, amount: int) -> list[Paper]:
        """Creates a HTTP request to search for titles using lexical search.

        Args:
            query (str): The query.
            amount (int): The amount of matches to return.

        Raises:
            ValueError: Is thrown if the length of the query is 0.
            ValueError: Is thrown if the amount of matches is negative.

        Returns:
            list[Paper]: The matches (list of instances of Paper).
        """
        Helper.ensure_type(query, str, "query must be a string!")
        Helper.ensure_type(amount, int, "amount must be an int!")

        if len(query) == 0:
            raise ValueError("query cannot be empty!")
        
        if amount < 0:
            raise ValueError("amount cannot be negative!")
        
        try:
            request_body = json.dumps({"query": query, "amount": amount})
            headers = {"Content-Type": "application/json"}
            response = requests.post(self.__config.backend_url + "/title/searchlex", data=request_body, headers=headers)
            response_json = response.json()
            result_list = response_json["result"]      
            result = self.__parse_search_by_title_lex_result_list(result_list)
            return result
        except Exception as e:
            raise

    
    def __parse_search_by_title_lex_result_list(self, result_list: list) -> list[Paper]:
        """Parses the response dictionary of a lexical search in titles to the corresponding classes.

        Args:
            result_list (list): The result list of response dictionaries.

        Returns:
            list[Paper]: List of parsed papers.
        """
        Helper.ensure_type(result_list, list, "result_list must be a list!")
        result = []

        for el in result_list:
            authors = [Author(e["fullName"]) for e in el["authors"]]
            paper = Paper(paper_id=el["paperId"], title=el["title"], abstract=el["abstract"], date_time=el["publicationDate"], authors=authors)
            result.append(paper)

        return result
    
    def __parse_search_by_title_result_list(self, result_list: list) -> list[Paper]:
        """Parses the response dictionary of a semantic search in titles to the corresponding classes.

        Args:
            result_list (list): The result list of response dictionaries.

        Returns:
            list[Paper]: List of corresponding papers.
        """
        Helper.ensure_type(result_list, list, "result_list must be a list!")
        result = []

        for el in result_list:
            authors = [Author(e["fullName"]) for e in el["authors"]]
            paper = Paper(paper_id=el["paperId"], title=el["title"], abstract=el["abstract"], date_time=el["publicationDate"], authors=authors)
            result.append(paper)

        return result
            
            
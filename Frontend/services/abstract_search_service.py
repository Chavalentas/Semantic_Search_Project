import json
import requests
from models.author import Author
from models.abstract_chunk import AbstractChunk
from models.paper_to_abstract_chunks import PaperToAbstractChunks
from models.helper import Helper
from models.paper import Paper
from config import Config


class AbstractSearchService:
    """A service containing functions to communicate with server to retrieve information about abstracts.
    """
    def __init__(self):
        """Initializes a new instance of AbstractSearchService.
        """
        self.__config = Config()

    def search_by_abstract_lexical(self, query: str, amount: int) -> list[Paper]:
        """Creates a HTTP request to search for abstracts using lexical search.

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
            response = requests.post(self.__config.backend_url + "/abstract/searchlex", data=request_body, headers=headers)
            response_json = response.json()
            result_list = response_json["result"]      
            result = self.__parse_search_by_abstract_lex_result_list(result_list)
            return result
        except Exception as e:
            raise

    def search_by_abstract(self, query: str, amount: int) -> list[PaperToAbstractChunks]:
        """Creates a HTTP request to search for abstracts using semantic search.

        Args:
            query (str): The query.
            amount (int): The amount of matches to return.

        Raises:
            ValueError: Is thrown if the length of the query is 0.
            ValueError: Is thrown if the amount of matches is negative.

        Returns:
            list[PaperToAbstractChunks]:  The matches (list of classes matching the corresponding chunk to its paper).
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
            response = requests.post(self.__config.backend_url + "/abstract/search", data=request_body, headers=headers)
            response_json = response.json()
            result_list = response_json["result"]      
            result = self.__parse_search_by_abstract_result_list(result_list)
            return result
        except Exception as e:
            raise

    def __parse_search_by_abstract_result_list(self, result_list: list) -> list[PaperToAbstractChunks]:
        """Parses the response dictionary of a semantic search in abstracts to the corresponding classes.

        Args:
            result_list (list): The result list of response dictionaries.

        Returns:
            list[PaperToAbstractChunks]: List of classes matching the abstract chunks to the paper.
        """
        Helper.ensure_type(result_list, list, "result_list must be a list!")
        result = []

        for el in result_list:
            paper_object = el["paper"]
            chunks_object = el["chunks"]
            authors = [Author(e["fullName"]) for e in paper_object["authors"]]
            paper = Paper(paper_id=paper_object["paperId"], title=paper_object["title"], abstract=paper_object["abstract"], date_time=paper_object["publicationDate"], authors=authors)
            abstract_chunks = []

            for chunk in chunks_object:
                abstract_chunks.append(AbstractChunk(paper_id=chunk["paperId"], text=chunk["chunkText"]))

            paper_to_abstract_chunks = PaperToAbstractChunks(paper=paper, chunks=abstract_chunks)
            result.append(paper_to_abstract_chunks)

        return result
    
    def __parse_search_by_abstract_lex_result_list(self, result_list: list) -> list[Paper]:
        """Parses the response dictionary of a lexical search in abstracts to the corresponding classes.

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
            
            


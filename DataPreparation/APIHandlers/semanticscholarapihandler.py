from APIHandlers.apihandler import APIHandler
from requests.adapters import HTTPAdapter
import requests
import json
import time
from Services.helper import Helper

class SemanticScholarBulkAPIHandler(APIHandler):
    """Represents the API handler that communicates with the API of Semantic Scholar.
    It fetches data in bulks.
    Args:
        APIHandler (_type_): The abstract API handler.
    """
    def __init__(self, query: str, max_papers_to_fetch: int):
        """Initializes a new instance of SemanticScholarBulkAPIHandler.

        Args:
            query (str): The API query.
            max_papers_to_fetch (int): The maximal amount of papers to fetch.
        """
        self.__set_query(query)
        self.__set_max_papers_to_fetch(max_papers_to_fetch)

    def fetch_data(self, url: str) -> dict:
        """Fetches data from the given URL.

        Args:
            url (str): The URL to fetch the data from.

        Returns:
            dict: The response as a dictionary.
            Format: {"semanticScholarPapers": [
               {"id": <paper-id>, "publicationDate": <publication-date>, "title": <paper-title>, "abstract": <paper-abstract>,
                 "authors": [{"fullName": <author-name>}, ...]},
                 ...
            ]}
        """
        Helper.ensure_type(url, str, "url must be a string!")
        
        adapter = HTTPAdapter()
        session = requests.Session()
        session.mount('https://', adapter)
        compose_url = f"{url}?query=\"{self.__query}\"&fields=title,abstract,authors,publicationDate"
        data = self.__retrieve_data(compose_url, session)
        result_list = self.__create_list(data)
        result = []
        result.extend(result_list)

        if not(self.__contains_token(data)):
            final_dict = {"semanticScholarPapers": result}
            return final_dict  
        
        token = self.__get_token(data)

        while (len(result) < self.__max_papers_to_fetch):
            compose_url = f"{url}?query=\"{self.__query}\"&fields=title,abstract,authors,publicationDate&token={token}"
            data = self.__retrieve_data(compose_url, session)
            result_list = self.__create_list(data)
            result.extend(result_list)

            if not(self.__contains_token(data)):
                break

        token = self.__get_token(data)


        final_dict = {"semanticScholarPapers": result}
        return final_dict
        
    def __set_query(self, query: str):
        """Sets the query to be used to fetch data from the API.

        Args:
            query (str): The API query.
        """
        Helper.ensure_type(query, str, "query must be a string!")
        self.__query = query
        
    def __set_max_papers_to_fetch(self, max_papers_to_fetch: int):
        """Sets the maximal amount of papers to fetch.

        Args:
            max_papers_to_fetch (int): The maximal amount of papers to fetch.

        Raises:
            ValueError: Is thrown if the maximal amount of papers to fetch is less or equal to 0.
        """
        Helper.ensure_type(max_papers_to_fetch, int, "max_papers_to_fetch must be an int!")
        
        if max_papers_to_fetch <= 0:
            raise ValueError("max_papers_to_fetch must be greater than 0!")
        
        self.__max_papers_to_fetch = max_papers_to_fetch

    def __create_data_dict(self, full_object: dict) -> dict: 
        """Creates a dictionary from the paper JSON object.
        Format: {"id": <paper-id>, "publicationDate": <publication-date>, "title": <paper-title>, "abstract": <paper-abstract>,
        "authors": [{"fullName": <author-name>}, ...]}.
        Args:
            full_object (dict): The JSON format of the paper entry.

        Returns:
            dict: The parsed dictionary.
        """
        Helper.ensure_type(full_object, dict, "full_object must be a dict!")
        
        title = full_object["title"]
        abstract = full_object["abstract"]
        paper_id = full_object["paperId"]
        publication_date = full_object["publicationDate"]
        author_names = [{"fullName": el["name"]} for el in full_object["authors"]]
        result_dict = {"id": paper_id, "title": title, "abstract": abstract, "publicationDate": publication_date, "authors": author_names}
        return result_dict
    
    def __retrieve_data(self, url: str, session: requests.Session):
        """Retrieves data from the given URL.

        Args:
            url (str): The session URL.
            session (requests.Session): The HTTP session.

        Returns:
            _type_: The retrieved data.
        """
        data = session.get(url)
        data.encoding = "utf-8"

        while data.status_code != 200:
            data = session.get(url)
            data.encoding = "utf-8"
        return data
    
    def __create_list(self, retrieved_data) -> list[dict]:
        """Creates a list of dictionaries containing
        the paper information.

        Args:
            retrieved_data (_type_): The retrieved data (JSON).

        Returns:
            list[dict]: The list of dictionaries.
            Format: {"id": <paper-id>, "publicationDate": <publication-date>, "title": <paper-title>, "abstract": <paper-abstract>,
            "authors": [{"fullName": <author-name>}, ...]}.
        """
        result_json = retrieved_data.json()
        result_str = json.dumps(result_json)
        result_dict = json.loads(result_str)
        data1 = result_dict["data"]
        result_list = [self.__create_data_dict(el) for el in data1]
        return result_list
    
    def __contains_token(self, retrieved_data) -> bool:
        """Returns a boolean indicating whether the retrieved JSON
        data contains a token indicating the continuation of bulk fetching.

        Args:
            retrieved_data (_type_): The retrieved data (JSON).

        Returns:
            bool: A boolean indicating whether the retrieved JSON
             data contains a token indicating the continuation of bulk fetching.
        """
        result_json = retrieved_data.json()
        result_str = json.dumps(result_json)
        result_dict = json.loads(result_str)
        return not(result_dict["token"] is None)
    
    def __get_token(self, retrieved_data) -> str:
        """Retrieves the token indicating the continuation of bulk fetching.

        Args:
            retrieved_data (_type_): The retrieved data (JSON).

        Returns:
            str: The token indicating the continuation of bulk fetching.
        """
        result_json = retrieved_data.json()
        result_str = json.dumps(result_json)
        result_dict = json.loads(result_str)
        return result_dict["token"]

                

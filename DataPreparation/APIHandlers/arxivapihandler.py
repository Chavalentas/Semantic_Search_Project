from APIHandlers.apihandler import APIHandler
from bs4 import BeautifulSoup
import requests
from Services.helper import Helper

class ArxivAPIHandler(APIHandler):
    """Represents the API handler that communicates with the API of arXiv.

    Args:
        APIHandler (_type_): The abstract API handler.
    """
    def __init__(self, query: str, papers_to_fetch: int, batch_size: int):
        """Initializes a new instance of ArxivAPIHandler.

        Args:
            query (str): The API query.
            papers_to_fetch (int): The amount of papers to fetch.
            batch_size (int): The batch size of the documents to fetch.
        """
        self.__set_query(query)
        self.__set_papers_to_fetch(papers_to_fetch)
        self.__set_batch_size(batch_size)

    def fetch_data(self, url: str) -> dict:
        """Fetches data from the given URL.

        Args:
            url (str): The URL to fetch the data from.

        Returns:
            dict: The response as a dictionary.
            Format: {"arxivPapers": [
               {"id": <paper-id>, "publicationDate": <publication-date>, "title": <paper-title>, "abstract": <paper-abstract>,
                 "authors": [{"fullName": <author-name>}, ...]},
                 ...
            ]}
        """
        Helper.ensure_type(url, str, "url must be a string!")
        
        start = 0
        b_size = self.__batch_size
        max_size = self.__papers_to_fetch
        result = []

        while start < max_size:
            compose_url = f"{url}?search_query=all:{self.__query}&start={str(start)}&max_results={str(b_size)}"
            data = requests.get(compose_url, headers={'Content-Type': 'application/atom+xml'})
            data = BeautifulSoup(data.content, "html")
            entries = data.find_all("entry")
            summary_dicts = [self.__create_entry_dict(el) for el in entries]
            result.extend(summary_dicts)
            start += b_size
        result_dict = {"arxivPapers": result}
        return result_dict
        
    def __set_query(self, query: str):
        """Sets the query to be used to fetch data from the API.

        Args:
            query (str): The API query.
        """
        Helper.ensure_type(query, str, "query must be a string!")
        
        self.__query = query
        
    def __set_papers_to_fetch(self, papers_to_fetch: int):
        """Sets the amount of papers to fetch.

        Args:
            papers_to_fetch (int): The amount of papers to fetch.

        Raises:
            ValueError: Is thrown if the amount of papers to fetch is 0 or less.
        """
        Helper.ensure_type(papers_to_fetch, int, "papers_to_fetch must be an int!")
        
        if papers_to_fetch <= 0:
            raise ValueError("papers_to_fetch must be greater than 0!")
        
        self.__papers_to_fetch = papers_to_fetch

    def __set_batch_size(self, batch_size: int):
        """Sets the batch size.

        Args:
            batch_size (int): The batch size.

        Raises:
            ValueError: Is throw if the batch size is 0 or less.
            ValueError: Is thrown if the batch size is bigger than the amount of papers to fetch.
        """
        Helper.ensure_type(batch_size, int, "batch_size must be an int!")
        
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0!")
        
        if batch_size > self.__papers_to_fetch:
            raise ValueError("batch_size cannot be greater than self.__papers_to_fetch!")
        
        self.__batch_size = batch_size

    def __format_text(self, input_text: str) -> str:
        """Formats the text (removes special characters like \\n).

        Args:
            input_text (str): The input text.

        Returns:
            str: The formatted text.
        """
        Helper.ensure_type(input_text, str, "input_text must be a string!")
        
        removed_nline = "".join([el if el != "\n" else " " for el in input_text])
        result = " ".join([el for el in removed_nline.split(" ") if el != ""])
        return result
    
    def __create_entry_dict(self, entry_xml) -> dict:
        """Creates a dictionary from the paper entry.
        Format: {"id": <paper-id>, "publicationDate": <publication-date>, "title": <paper-title>, "abstract": <paper-abstract>,
        "authors": [{"fullName": <author-name>}, ...]}.
        Args:
            entry_xml (_type_): The XML format of the paper entry.

        Returns:
            dict: The parsed dictionary.
        """
        paper_id = self.__format_text(entry_xml.find_all("id")[0].text)
        publication_date = self.__format_text(entry_xml.find_all("published")[0].text)
        title = self.__format_text(entry_xml.find_all("title")[0].text)
        summary = self.__format_text(entry_xml.find_all("summary")[0].text)
        authors = entry_xml.find_all("author")
        author_names = [{"fullName": self.__format_text(a.find_all("name")[0].text)} for a in authors]
        return {"id": paper_id, "publicationDate": publication_date, "title": title, "abstract": summary, "authors": author_names}
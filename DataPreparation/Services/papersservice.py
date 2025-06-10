from Services.mongodbservice import MongoDBService
from Services.helper import Helper
import pandas as pd

class PapersService(MongoDBService):
    """Represents a service that deals with data from MongoDB.
    It communicates with a collection that stores information about the papers.

    Args:
        MongoDBService (_type_): Service that communicates with MongoDB database. 
    """
    def __init__(self, url):
        """Initializes a new instance of PapersService.

        Args:
            url (str): The URL of the MongoDB cluster.
        """
        MongoDBService.__init__(self, url)

    def insert_papers(self, dict_papers: list[dict]):
        """Inserts papers into MongoDB database.

        Args:
            dict_papers (list[dict]): The paper information stored as list of dictionaries.
        """
        Helper.ensure_list_of_type(dict_papers, dict, "dict_papers must be a list!", "dict_papers must contain elements of type dict!")
        
        self.insert_data("papersDB", "papers", dict_papers)

    def get_papers(self, query: dict) -> list:
        """Fetches the papers specified by a query.

        Args:
            query (dict): The query in dictionary format.

        Returns:
            list: A list including dictionaries of fetched data.
        """
        return self.get_data("papersDB", "papers", query)

    def get_papers_as_df(self):
        """Retrieves all papers as a data frame.

        Returns:
            DataFrame: A Pandas data frame.
        """
        client = self.get_client()
        db = client["papersDB"]
        collection = db["papers"]
        ids = []
        titles = []
        abstracts = []
        authors = []
        publication_dates = []

        for document in collection.find({}):
            ids.append(document["id"])
            titles.append(document["title"])
            abstracts.append(document["abstract"])
            abstracts.append(document["publicationDate"])
            authors.append(",".join([el["fullName"] for el in document["authors"]]))

        result_frame = pd.DataFrame({"id": ids, "title": titles, "publicationDate": publication_dates, "abstract": abstracts, "authors":  authors})
        return result_frame
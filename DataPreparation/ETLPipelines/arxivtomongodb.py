import os
from ETLPipelines.pipeline import ETLPipeline
from APIHandlers.arxivapihandler import ArxivAPIHandler
from DataPreparators.arxivdatapreparator import ArxivDataPreparator
from Services.papersservice import PapersService
from dotenv import load_dotenv

class ArxivToMongoDBPipeline(ETLPipeline):
    """Represents a pipeline that pipes data from the arXiv API to a
    MongoDB cluster.

    Args:
        ETLPipeline (_type_): The abstract base class.
    """
    def __init__(self, api_url: str, search_query: str, papers_to_fetch: int, batch_size: int):
        """Initializes a new instance of ArxivToMongoDBPipeline.

        Args:
            api_url (str): The URL of the arXiv API.
            search_query (str): The search query for the arXiv API.
            papers_to_fetch (int): The amount of papers to fetch from the arXiv API.
            batch_size (int): The batch size of the fetch result.
        """
        self.api_url = api_url
        self.search_query = search_query
        self.papers_to_fetch = papers_to_fetch
        self.batch_size = batch_size
        
    def extract(self):
        """Extracts the data from the arXiv API.
        """
        api_handler = ArxivAPIHandler(self.search_query, self.papers_to_fetch, self.batch_size)
        data = api_handler.fetch_data(self.api_url)
        self.extracted_data = data

    def transform(self):
        """Transforms the data fetched from the arXiv API.
        Removes empty titles, abstracts and duplicate papers.
        """
        data_preparator = ArxivDataPreparator(self.papers_to_fetch, True, True)
        prepared = data_preparator.prepare_data(self.extracted_data)
        self.prepared_data = prepared        

    def load(self):
        """Loads the transformed papers to a MongoDB cluster.
        """
        load_dotenv()
        url = os.getenv("MONGODB_URL")
        db_service = PapersService(url)
        db_service.insert_papers(self.prepared_data["arxivPapers"])
        
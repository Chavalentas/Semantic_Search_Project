import os
from dotenv import load_dotenv
from ETLPipelines.pipeline import ETLPipeline
from APIHandlers.semanticscholarapihandler import SemanticScholarBulkAPIHandler
from DataPreparators.semscholarbulkdatapreparator import SemanticScholarBulkDataPreparator
from Services.papersservice import PapersService
from DataPreparators.semscholarbulkdatapreparator import SemanticScholarBulkDataPreparator

class SemanticScholarToMongoDBPipeline(ETLPipeline):
    """Represents a pipeline that pipes data from the Semantic Scholar API to a
    MongoDB cluster.

    Args:
        ETLPipeline (_type_): The abstract base class.
    """
    def __init__(self, api_url: str, search_query: str, papers_to_fetch: int, papers_to_load: int):
        """Initializes a new instance of SemanticScholarToMongoDBPipeline.

        Args:
            api_url (str): The URL of the Semantic Scholar API.
            search_query (str): The search query for the Semantic Scholar API.
            papers_to_fetch (int): The amount of papers to fetch from the Semantic Scholar API.
            papers_to_load (int): The amount of papers to load to the MongoDB cluster.
        """
        self.api_url = api_url
        self.search_query = search_query
        self.papers_to_fetch = papers_to_fetch
        self.papers_to_load = papers_to_load
        
    def extract(self):
        """Extracts the data from the Semantic Scholar API.
        """
        api_handler = SemanticScholarBulkAPIHandler(self.search_query, self.papers_to_fetch)
        data = api_handler.fetch_data(self.api_url)
        self.extracted_data = data

    def transform(self):
        """Transforms the data fetched from the Semantic Scholar API.
        Removes empty titles, abstracts and duplicate papers.
        """
        data_preparator = SemanticScholarBulkDataPreparator(self.papers_to_load, True, True)
        prepared = data_preparator.prepare_data(self.extracted_data)
        self.prepared_data = prepared        

    def load(self):
        """Loads the transformed papers to a MongoDB cluster.
        """
        load_dotenv()
        url = os.getenv("MONGODB_URL")
        db_service = PapersService(url)
        db_service.insert_papers(self.prepared_data["semanticScholarPapers"])
        
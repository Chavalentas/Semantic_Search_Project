from models.helper import Helper
from services.mongodbservice import MongoDBService

class TitleChunksService(MongoDBService):
    """Represents a service that deals with data from MongoDB.
    It communicates with a collection that stores information about the title chunks.

    Args:
        MongoDBService (_type_): Service that communicates with MongoDB database.
    """
    def __init__(self, url):
        """Initializes a new instance of TitleChunksService.

        Args:
            url (str): The URL of the MongoDB cluster.
        """
        MongoDBService.__init__(self, url)    

    def insert_chunks(self, dict_chunks: list[dict]):
        """Inserts title chunks into MongoDB database.

        Args:
            dict_chunks (list[dict]): The chunk information stored as list of dictionaries.
        """
        Helper.ensure_list_of_type(dict_chunks, dict, "dict_chunks must be a list!", "dict_chunks must contain elements of type dict!")         
        self.insert_data("papersDB", "titleChunks", dict_chunks)

    def insert_chunks_in_batch(self, dict_chunks: list[dict], batch_size: int):
        """Inserts title chunks in batches of specific size.

        Args:
            dict_chunks (list[dict]): The chunk information stored as list of dictionaries.
            batch_size (int): The batch size. 

        Raises:
            ValueError: Is thrown if batch_size is either 0 or negative.
        """
        Helper.ensure_list_of_type(dict_chunks, dict, "dict_chunks must be a list!", "dict_chunks must contain elements of type dict!")
        Helper.ensure_type(batch_size, int, "batch_size must be an int!")

        if batch_size <= 0:
            raise ValueError("batch_size cannot be less or equal to 0!")
        
        self.insert_data_batch("papersDB", "titleChunks", dict_chunks, batch_size)

    def aggregate_data(self, aggregation_data: list[dict]):
        """Aggregates the data using specific operations.

        Args:
            aggregation_data (list[dict]): Aggregation operations stored as a list of dictionaries.

        Returns:
            _type_: The aggregated result.
        """
        Helper.ensure_list_of_type(aggregation_data, dict, "aggregation_data must be a list!", "aggregation_data must contain elements of type dict!")
        
        return  MongoDBService.aggregate_data(self, "papersDB", "titleChunks", aggregation_data)

    def get_chunks(self, query: dict) -> list:
        """Fetches the title chunks specified by a query.

        Args:
            query (dict): The query in dictionary format.

        Returns:
            list: A list including dictionaries of fetched data.
        """
        return self.get_data("papersDB", "titleChunks", query)
    
    def create_search_index(self, index_data: dict):
        """Creates a search index using specific index data.

        Args:
            index_data (dict): Index data stored as a dictionary.
        """
        Helper.ensure_type(index_data, dict, "index_data must be a dict!")
        
        MongoDBService.create_search_index(self, "papersDB", "titleChunks", index_data)
from Services.helper import Helper
import pymongo

class MongoDBService:
    """Represents a service that communicates with a MongoDB cluster.
    """
    def __init__(self, url):
        """Initializes a new instance of MongoDBService.

        Args:
            url (str): The URL of the MongoDB cluster.
        """
        self.__set_url(url)

    def get_client(self) -> pymongo.MongoClient:
        """Creates a MongoDB connection client.

        Returns:
            MongoClient: A MongoDB client.
        """
        client = pymongo.MongoClient(self.__url)
        return client
    
    def create_search_index(self, db_name: str, collection_name: str, index_dict: dict):
        """Creates a new search index.

        Args:
            db_name (str): The name of the MongoDB database.
            collection_name (str): The collection name.
            index_dict (dict): The index information as a dictionary.

        Raises:
            e: Error that occurred during the creation of the search index.
        """
        Helper.ensure_type(db_name, str, "db_name must be a string!")
        Helper.ensure_type(collection_name, str, "collection_name must be a string!")
        Helper.ensure_type(index_dict, dict, "index_dict must be a dict!")
        
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            collection.create_search_index(index_dict)
        except Exception as e:
            raise e
        
    
    def insert_data(self, db_name: str, collection_name: str, data: list[dict]):
        """Inserts data into a database of a MongoDB cluster.

        Args:
            db_name (str):  The name of the MongoDB database.
            collection_name (str): The collection name.
            data (list[dict]): The data objects as dictionaries.

        Raises:
            e: Error that occurred during the operation.
        """
        Helper.ensure_type(db_name, str, "db_name must be a string!")
        Helper.ensure_type(collection_name, str, "collection_name must be a string!")
        Helper.ensure_list_of_type(data, dict, "data must be a list!", "data must contain elements of type dict!")
        
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            collection.insert_many(data)
        except Exception as e:
            raise e
        
    def aggregate_data(self, db_name: str, collection_name: str, aggregation_data: list[dict]):
        """Aggregates data using specific aggregation operations.

        Args:
            db_name (str):  The name of the MongoDB database.
            collection_name (str): The collection name.
            aggregation_data (list[dict]): The aggregation information as dictionaries.

        Raises:
            e: Error that occurred during the operation.

        Returns:
            _type_: The aggregated results.
        """
        Helper.ensure_type(db_name, str, "db_name must be a string!")
        Helper.ensure_type(collection_name, str, "collection_name must be a string!")
        Helper.ensure_list_of_type(aggregation_data, dict, "aggregation_data must be a list!", "aggregation_data must contain elements of type dict!")
        
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            results = collection.aggregate(aggregation_data)
            return results
        except Exception as e:
            raise e
        
    def insert_data_batch(self, db_name: str, collection_name: str, data: list[dict], batch_size: int):
        """Inserts data in batches of specific size. 

        Args:
            db_name (str): The name of the MongoDB database.
            collection_name (str): The collection name.
            data (list[dict]):  The data stored as list of dictionaries.
            batch_size (int): The batch size. 

        Raises:
            ValueError: Is thrown if batch_size is either 0 or negative.
        """
        Helper.ensure_type(db_name, str, "db_name must be a string!")
        Helper.ensure_type(collection_name, str, "collection_name must be a string!")
        Helper.ensure_list_of_type(data, dict, "data must be a list!", "data must contain elements of type dict!")
        Helper.ensure_type(batch_size, int, "batch_size must be an int!")

        if batch_size <= 0:
            raise ValueError("batch_size cannot be less or equal to 0!")
        
        client = self.get_client()
        db = client[db_name]
        collection = db[collection_name]
        data_length = len(data)
        iteration_count = data_length // batch_size

        if data_length % batch_size > 0:
            iteration_count += 1

        current_index = 0
        for i in range(iteration_count):
            collection.insert_many(data[current_index:current_index + batch_size])
            current_index += batch_size
        
    def insert_one_data(self, db_name: str, collection_name: str, data: dict):
        """Inserts one data specified as a dictionary.

        Args:
            db_name (str): The name of the MongoDB database.
            collection_name (str): The collection name.
            data (dict): The data to insert as a dictionary.

        Raises:
            e: Error that occurred during the operation.
        """
        Helper.ensure_type(db_name, str, "db_name must be a string!")
        Helper.ensure_type(collection_name, str, "collection_name must be a string!")
        Helper.ensure_type(data, dict, "data must be a dict!")
        
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            collection.insert_one(data)
        except Exception as e:
            raise e
        
        
    def get_data(self, db_name: str, collection_name: str, query: dict) -> list:
        """Fetches data from the MongoDB database.

        Args:
            db_name (str): The name of the MongoDB database.
            collection_name (str): The collection name.
            query (dict): The query specified as a dictionary.

        Raises:
            e: Error that occurred during the operation.

        Returns:
            list: A list of retrieved results.
        """
        Helper.ensure_type(db_name, str, "db_name must be a string!")
        Helper.ensure_type(collection_name, str, "collection_name must be a string!")
        
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            result = collection.find(query)
            return list(result)
        except Exception as e:
            raise e

    
    def __set_url(self, url: str):
        """Sets the URL of the MongoDB cluster.

        Args:
            url (str): The URL.
        """
        Helper.ensure_type(url, str, "url must be a string!")
        
        self.__url = url
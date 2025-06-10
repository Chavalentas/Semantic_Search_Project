from Services.preprocessingservice import PreprocessingService
from Services.embeddingservice import EmbeddingService
from ETLPipelines.pipeline import ETLPipeline
import os
import nltk
from dotenv import load_dotenv
from Services.abstractchunksservice import AbstractChunksService
from Services.helper import Helper
from Services.papersservice import PapersService

class MongoDBPapersToAbstractChunksPipeline(ETLPipeline):
    """Represents a pipeline that fetches papers from MongoDB
    and creates vector embeddings for the chunks of the papers' abstracts.
    Afterwards, the data is loaded into a new collection.
    Args:
        ETLPipeline (_type_): The abstract base class.
    """
    def __init__(self, embedding_service: EmbeddingService, preprocessing_service: PreprocessingService, batch_size: int, nltk_path: str):
        """Initializes a new instance of MongoDBPapersToAbstractChunksPipeline.

        Args:
            embedding_service (EmbeddingService): The embedding service used to generate vectors.
            preprocessing_service (PreprocessingService): The preprocessing service used to preprocess the abstract chunks.
            batch_size (int): The batch size used to load the preprocessed and embedded abstract chunks into a new collection.
            nltk_path (str): The path to the nltk library.
        """
        self.embedding_service = embedding_service
        self.preprocessing_service = preprocessing_service
        self.batch_size = batch_size
        nltk.data.path.append(nltk_path)

    def extract(self):
        """Extracts the papers from MongoDB.
        """
        load_dotenv()
        url = os.getenv("MONGODB_URL")
        db_service = PapersService(url)
        papers = db_service.get_papers({})
        self.extracted_papers = papers

    def transform(self):
        """Splits the papers' abstracts into smaller chunks.
        The chunks are sentences (English is supported).
        Preprocesses the chunks.
        Removes duplicate chunks from the preprocessing result.
        Creates embeddings for the chunks.
        """
        papers = self.extracted_papers
        id_to_abstract_chunks = [{"id": el["id"], "chunks": nltk.sent_tokenize(el["abstract"], language="english")} for el in papers]
        id_to_abstract_chunks = self.__preprocess_chunks(id_to_abstract_chunks)
        id_to_abstract_chunks_embedded = self.__generate_chunk_embeddings(id_to_abstract_chunks)
        self.data_to_insert = self.__explode_chunk_embeddings(id_to_abstract_chunks_embedded)
        self.data_to_insert = Helper.remove_duplicate_entries(self.data_to_insert, "chunk")

    def load(self):
        """Loads the preprocessed chunks to a new MongoDB collection.
        Creates a search index for the embedding vectors (specified by the collection's attribute of the vector).
        """
        load_dotenv()
        url = os.getenv("MONGODB_URL")
        db_service = AbstractChunksService(url)
        db_service.insert_chunks_in_batch(self.data_to_insert, self.batch_size)
        db_service.create_search_index({
            "definition": {
                "mappings":{
                    "dynamic": True,
                    "fields": {
                        "chunkVector": {
                            "dimensions": 384,
                            "similarity": "cosine",
                            "type": "knnVector",
                        }
                    }
                }
            },
            "name": "AbstractSearchIndex"
        })

    def __generate_chunk_embeddings(self, id_to_sentences_dict: list[dict]) -> list[dict]:
        """Generates vector embeddings for the chunks.

        Args:
            id_to_sentences_dict (list[dict]): A list of dictionaries.
            Format: [{"id": <paper-id>, "chunks": ["chunk1", ...], "preprocessed": ["preprocessed1", ...]}, ...].
        Returns:
            list[dict]: A list of dictionaries.
            Format: [{"id": <paper-id>, "chunks": ["chunk1", ...], "preprocessed": ["preprocessed1", ...], 
            "embedded": ["embedded1", ...]}, ...].
        """
        result = id_to_sentences_dict

        for el in result:
            el["embedded"] = [self.embedding_service.create_embedding(chunk) for chunk in el["preprocessed"]]

        return result
    
    def __preprocess_chunks(self, id_to_sentences_dict: list[dict]) -> list[dict]:
        """Preprocesses the chunks.

        Args:
            id_to_sentences_dict (list[dict]): A list of dictionaries.
            Format: [{"id": <paper-id>, "chunks": ["chunk1", ...]}, ...].
        Returns:
            list[dict]: A list of dictionaries.
            Format: [{"id": <paper-id>, "chunks": ["chunk1", ...], "preprocessed": ["preprocessed1", ...]}, ...].
        """
        result = id_to_sentences_dict

        for el in result:
            el["preprocessed"] = [self.preprocessing_service.preprocess(chunk) for chunk in el["chunks"]]

        return result
    
    def __explode_chunk_embeddings(self, id_to_abstract_chunks_embeddings: list[dict]) -> list[dict]:
        """Explodes the chunk embeddings.
        For every embedding in the list, e new dictionary containing the paper ID and the chunk embedding will be created.

        Args:
            id_to_abstract_chunks_embeddings (list[dict]): A list of dictionaries.
            Format: [{"id": <paper-id>, "chunks": ["chunk1", ...], "preprocessed": ["preprocessed1", ...], 
            "embedded": ["embedded1", ...]}, ...].
        Returns:
            list[dict]: A list of dictionaries.
            Format:  [{"paperId": <paper-id>, "chunk": <chunk>, "chunkVector": <embedding-vector>}, ...].
        """
        result = []

        for el in id_to_abstract_chunks_embeddings:
            for i, chunk in enumerate(el["chunks"]):
                to_append = {"paperId": el["id"], "chunk": chunk, "chunkVector": [float(e) for e in el["embedded"][i]]}
                result.append(to_append)

        return result



        
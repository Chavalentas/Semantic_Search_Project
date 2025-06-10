import os
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer, SimilarityFunction
from services.basicenglishpreprocessingservice import BasicEnglishPreprocessingService
from services.conversionservice import ConversionService
from services.abstractchunksservice import AbstractChunksService
from services.transfomerembeddingservice import TransformerEmbeddingService
from models.base_models.author import Author
from models.base_models.paper import Paper
from models.helper import Helper
from models.response_bodies.abstractsearch_lex_responsebody import AbstractSearchLexResponseBody
from services.papersservice import PapersService
from models.response_bodies.abstractsearch_responsebody import AbstractSearchResponseBody
from models.request_bodies.abstractsearch_requestbody import AbstractSearchRequestBody
from models.request_bodies.abstractsearch_lex_requestbody import AbstractSearchLexRequestBody
import nltk
from nltk.corpus import stopwords
nltk.data.path.append("./tokenizers")
nltk.download("punkt", download_dir="./tokenizers")
nltk.download("stopwords", download_dir="./tokenizers")
nltk.download('punkt_tab', download_dir="./tokenizers")

# Load services
load_dotenv()
url = os.getenv("MONGODB_URL")
papers_service = PapersService(url)
abstract_chunks_service = AbstractChunksService(url)
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", similarity_fn_name=SimilarityFunction.COSINE)
embeddings_service = TransformerEmbeddingService(embedder)
stopwords = list(set(stopwords.words('english')))
preprocessing_service = BasicEnglishPreprocessingService(stopwords)
conversion_service = ConversionService()

# Initialize the router
router = APIRouter(prefix="/abstract")

@router.post("/search", status_code=200, response_model=AbstractSearchResponseBody)
async def search_by_abstract(request_body: AbstractSearchRequestBody) -> JSONResponse:
    """Performs a semantic search in the papers' abstracts.

    Args:
        request_body (AbstractSearchRequestBody): The request body of the controller.

    Returns:
        _type_: The response of the controller.
        {"message": <content>} if error, AbstractSearchResponseBody otherwise.
    """
    if request_body == None:
        return JSONResponse(status_code=400, content={"message": "Empty request body!"})
    if not(isinstance(request_body, AbstractSearchRequestBody)):
        return JSONResponse(status_code=400, content={"message": "Wrong format of the request body!"})
    if not(type(request_body.amount) == int):
        return JSONResponse(status_code=400, content={"message": "Amount of results has to be a number!"})
    if request_body.amount < 0:
        return JSONResponse(status_code=400, content={"message": "Amount of results cannot be negative!"})
    if not(type(request_body.query) == str):
        return JSONResponse(status_code=400, content={"message": "Query has to be a string!"})
    if len(request_body.query) == 0:
        return JSONResponse(status_code=400, content={"message": "Query cannot be empty!"})  

    try:
        query_preprocessed = preprocessing_service.preprocess(request_body.query)
        query_embedded = embeddings_service.create_embedding(query_preprocessed)

        results = abstract_chunks_service.aggregate_data([
            {"$vectorSearch": {
                "queryVector": query_embedded,
                "path": "chunkVector",
                "numCandidates": 100,
                "limit": request_body.amount,
                "index": "AbstractSearchIndex",
                }
            },
            {
                "$project":{
                    "_id": 0,
                    "chunkVector": 0
                }
            }  
        ])
        
        copy_list = list(results).copy()
        result_papers = papers_service.get_papers({"id": {"$in": [el["paperId"] for el in copy_list]}})
        response_list = conversion_service.paper_abstract_chunks_to_class_object(result_papers, copy_list)
        response = AbstractSearchResponseBody(result=response_list)
        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal error: " + str(e)}) 
    

@router.post("/searchlex", status_code=200, response_model=AbstractSearchLexResponseBody)
async def search_by_abstract_lex(request_body: AbstractSearchLexRequestBody) -> JSONResponse:
    """Performs a lexical search in the papers' abstracts.

    Args:
        request_body (AbstractSearchLexRequestBody): The request body of the controller.

    Returns:
        _type_: The response of the controller.
        {"message": <content>} if error, AbstractSearchLexResponseBody otherwise.
    """
    if request_body == None:
        return JSONResponse(status_code=400, content={"message": "Empty request body!"})
    if not(isinstance(request_body, AbstractSearchLexRequestBody)):
        return JSONResponse(status_code=400, content={"message": "Wrong format of the request body!"})
    if not(type(request_body.amount) == int):
        return JSONResponse(status_code=400, content={"message": "Amount of results has to be a number!"})
    if request_body.amount < 0:
        return JSONResponse(status_code=400, content={"message": "Amount of results cannot be negative!"})
    if not(type(request_body.query) == str):
        return JSONResponse(status_code=400, content={"message": "Query has to be a string!"})
    if len(request_body.query) == 0:
        return JSONResponse(status_code=400, content={"message": "Query cannot be empty!"})   
    
    try:
        query = request_body.query
        amount = request_body.amount
        results = papers_service.get_papers({})
        ids = [el["id"] for el in results]
        abstracts = [el["abstract"] for el in results]
        match_counts = [Helper.get_match_count(query, abstract) for abstract in abstracts]
        list_zipped = list(zip(ids, abstracts, match_counts))
        list_zipped = [el for el in list_zipped if el[2] != 0]
        list_zipped = sorted(list_zipped, key=lambda x: x[2], reverse=True)
        list_zipped = list_zipped[:amount]
        ids = [el[0] for el in list_zipped]
        papers_to_return = list(map(lambda x: [el for el in results if el["id"] == x][0], ids))
        papers = [Paper(paperId=el["id"], title=el["title"], abstract=el["abstract"], publicationDate=str(el["publicationDate"]), authors=[Author(fullName=e["fullName"]) for e in el["authors"]]) for el in papers_to_return]
        response = AbstractSearchLexResponseBody(result=papers)
        return response 
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal error: " + str(e)})
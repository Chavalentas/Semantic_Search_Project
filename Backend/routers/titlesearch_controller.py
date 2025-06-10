import os
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer, SimilarityFunction
from services.basicenglishpreprocessingservice import BasicEnglishPreprocessingService
from services.conversionservice import ConversionService
from services.transfomerembeddingservice import TransformerEmbeddingService
from services.titlechunksservice import TitleChunksService
from models.base_models.author import Author
from models.base_models.paper import Paper
from models.helper import Helper
from services.papersservice import PapersService
from models.request_bodies.titlesearch_lex_requestbody import TitleSearchLexRequestBody
from models.response_bodies.titlesearch_lex_responsebody import TitleSearchLexResponseBody
from models.request_bodies.titlesearch_requestbody import TitleSearchRequestBody
from models.response_bodies.titlesearch_responsebody import TitleSearchResponseBody
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
title_chunks_service = TitleChunksService(url)
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", similarity_fn_name=SimilarityFunction.COSINE)
embeddings_service = TransformerEmbeddingService(embedder)
stopwords = list(set(stopwords.words('english')))
preprocessing_service = BasicEnglishPreprocessingService(stopwords)
conversion_service = ConversionService()

# Initialize the router
router = APIRouter(prefix="/title")

@router.post("/search", status_code=200, response_model=TitleSearchResponseBody)
async def search_by_title(request_body: TitleSearchRequestBody) -> JSONResponse:
    """Performs a semantic search in the papers' titles.

    Args:
        request_body (TitleSearchRequestBody): The request body of the controller.

    Returns:
        _type_: The response of the controller.
        {"message": <content>} if error, TitleSearchResponseBody otherwise.
    """
    try:
        query_preprocessed = preprocessing_service.preprocess(request_body.query)
        query_embedded = embeddings_service.create_embedding(query_preprocessed)

        results = title_chunks_service.aggregate_data([
            {"$vectorSearch": {
                "queryVector": query_embedded,
                "path": "chunkVector",
                "numCandidates": 100,
                "limit": request_body.amount,
                "index": "TitleSearchIndex",
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
        response_list = conversion_service.paper_title_chunks_to_class_object(result_papers, copy_list)
        response = TitleSearchResponseBody(result=response_list)
        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal error: " + str(e)}) 

@router.post("/searchlex", status_code=200, response_model=TitleSearchLexResponseBody)
async def search_by_title_lex(request_body: TitleSearchLexRequestBody) -> JSONResponse:
    """Performs a lexical search in the papers' titles.

    Args:
        request_body (TitleSearchLexRequestBody): The request body of the controller.

    Returns:
        _type_: The response of the controller.
        {"message": <content>} if error, TitleSearchLexResponseBody otherwise.
    """
    if request_body == None:
        return JSONResponse(status_code=400, content={"message": "Empty request body!"})
    if not(isinstance(request_body, TitleSearchLexRequestBody)):
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
        titles = [el["title"] for el in results]
        match_counts = [Helper.get_match_count(query, title) for title in titles]
        list_zipped = list(zip(ids, titles, match_counts))
        list_zipped = [el for el in list_zipped if el[2] != 0]
        list_zipped = sorted(list_zipped, key=lambda x: x[2], reverse=True)
        list_zipped = list_zipped[:amount]
        ids = [el[0] for el in list_zipped]
        papers_to_return = list(map(lambda x: [el for el in results if el["id"] == x][0], ids))
        papers = [Paper(paperId=el["id"], title=el["title"], abstract=el["abstract"], publicationDate=str(el["publicationDate"]), authors=[Author(fullName=e["fullName"]) for e in el["authors"]]) for el in papers_to_return]
        response = TitleSearchLexResponseBody(result=papers)
        return response 
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal error: " + str(e)})
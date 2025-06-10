from models.helper import Helper
from models.base_models.abstract_chunk import AbstractChunk
from models.base_models.author import Author
from models.base_models.paper import Paper
from models.base_models.paper_to_abstract_chunks import PaperToAbstractChunks


class ConversionService:
    """Represents a service that converts between classic Python objects and pydantic Base models.
    """
    def paper_abstract_chunks_to_class_object(self, papers: list[dict], paper_id_chunk_dicts: list[dict]) -> list[PaperToAbstractChunks]:
        """Converts dictionaries containing abstract chunks to a specific pydantic Base model.

        Args:
            papers (list[dict]): Paper information as list of dictionaries.
            Dictionary format: {"id": <paper-id>, "title": <paper-title>, "abstract": <paper-abstract>, "publicationDate": <paper-publication-date>,
            "authors": [{"fullName": <name>}, ...]}.
            paper_id_chunk_dicts (list[dict]): Mapping dictionary between papers and abstract chunks.
            Dictionary format: {"paperId": <paper-id>, "chunkText": <chunk-text>}.

        Returns:
            list[PaperToAbstractChunks]: List of instances of PaperToAbstractChunks.
        """
        Helper.ensure_list_of_type(papers, dict, "papers must be a list!", "papers must contain elements of type dict!")  
        Helper.ensure_list_of_type(paper_id_chunk_dicts, dict, "paper_id_chunk_dicts must be a list!", "paper_id_chunk_dicts must contain elements of type dict!")          
        result = []

        for ch_dict in paper_id_chunk_dicts:
            paper = [el for el in papers if el["id"] == ch_dict["paperId"]][0]
            paper_obj = Paper(paperId=paper["id"],  title=paper["title"], abstract=paper["abstract"], publicationDate=str(paper["publicationDate"]),
                              authors=[Author(fullName=e["fullName"]) for e in paper["authors"]])
            chunk = AbstractChunk(paperId=ch_dict["paperId"], chunkText=ch_dict["chunk"])
            to_append = PaperToAbstractChunks(paper=paper_obj, chunks=[chunk])
            result.append(to_append)

        return result
    
    def paper_title_chunks_to_class_object(self, papers: list[dict], paper_id_chunk_dicts: list[dict]) -> list[Paper]:
        """Filters out papers that match the given chunks and returns
        them as a list of the corresponding pydantic Base models.

        Args:
            papers (list[dict]): Paper information as list of dictionaries.
            Dictionary format: {"id": <paper-id>, "title": <paper-title>, "abstract": <paper-abstract>, "publicationDate": <paper-publication-date>,
            "authors": [{"fullName": <name>}, ...]}.
            paper_id_chunk_dicts (list[dict]): _ Mapping dictionary between papers and abstract chunks.
            Dictionary format: {"paperId": <paper-id>, "chunkText": <chunk-text>}.

        Returns:
            list[Paper]: List of instances of Paper.
        """
        Helper.ensure_list_of_type(papers, dict, "papers must be a list!", "papers must contain elements of type dict!")  
        Helper.ensure_list_of_type(paper_id_chunk_dicts, dict, "paper_id_chunk_dicts must be a list!", "paper_id_chunk_dicts must contain elements of type dict!")                  
        result = []

        for ch_dict in paper_id_chunk_dicts:
            paper = [el for el in papers if el["id"] == ch_dict["paperId"]][0]
            paper_obj = Paper(paperId=paper["id"],  title=paper["title"], abstract=paper["abstract"], publicationDate=str(paper["publicationDate"]),
                              authors=[Author(fullName=e["fullName"]) for e in paper["authors"]])
            result.append(paper_obj)

        return result
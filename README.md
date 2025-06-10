# Semantic_Search_Project
This document describes the project that represents a semantic search engine
specialized in papers that deal with long-term care.
The following describes the structure of the project with the description of its parts.

## Used technologies
![Jupyter](https://img.shields.io/badge/Jupyter-%23e7ebc7?style=for-the-badge&logo=Jupyter) 
![Python](https://img.shields.io/badge/Python-yellow?style=for-the-badge&logo=Python)
![FastAPI](https://img.shields.io/badge/FastAPI-green?style=for-the-badge&logo=FastAPI)
![Gradio](https://img.shields.io/badge/Gradio-orange?style=for-the-badge&logo=Gradio)
![MongoDB](https://img.shields.io/badge/MongoDB-%23abb9cf?style=for-the-badge&logo=mongodb)

## Used paper sources
The following picture depicts the scientific paper sources used 
to fetch and prepare scientific papers.
The picture also depicts the data exchange formats of their APIs.
![data_sources](img/data_sources.png)


## DataPreparation
This folder contains code that was used to prepare data for the semantic search engine.
Also different models (sentence transformers) were compared.
```
│   
│      
│
└───APIHandlers
│   
│   
└───DataPreparators
│   
│       
└───ETLPipelines
│
│
└───Services
│
│
|   
│   main.ipynb
```

### main.ipynb
The main description of the data preparation.
**Please read this notebook**.
The notebook contains information about pipelines and preparation steps
that were undertaken to prepare the data for the semantic search engine.
All modules in the subfolders of the project were explained in the code documentation.
**Please do not execute this notebook again.**


### APIHandlers
This folder contains modules that communicate with APIs of external scientific paper databases (arXiv and Semantic Scholar).

### DataPreparators
This folder contains modules that prepare data fetched using API handlers from scientific paper databases (arXiv and Semantic Scholar).

### ETLPipelines
This folder contains ETL pipelines used to extract, transform and load different kinds of data.
The following pipelines were implemented.
* arXiv API (Extract) -> Remove duplicate papers and papers with missing titles and abstracts (Transform) -> Load papers to MongoDB (Load)
![pipeline_1](img/arxiv_mongo_db_etl.png)
* Semantic Scholar API (Extract) -> Remove duplicate papers and papers with missing titles and abstracts (Transform) -> Load papers to MongoDB (Load)
![pipeline_2](img/semantic_scholar_mongo_db_etl.png)
* MongoDB Papers (Extract) -> Perform abstract chunking, chunk preprocessing, chunk embedding (Transform) -> Load chunks to MongoDB (Load)
![pipeline_3](img/mongo_db_to_abstract_chunks_etl.drawio.png)
* MongoDB Papers (Extract) -> Perform title chunking, chunk preprocessing, chunk embedding (Transform) -> Load chunks to MongoDB (Load)
![pipeline_4](img/mongo_db_to_title_chunks_etl.png)

### Services
This folder contains modules that encapsulate the business logic used to communicate with the MongoDB database,
to preprocess data and to embed data.

## ER diagram of the MongoDB database model
The following picture depicts how data (papers and their title and abstract chunks)
was stored in the MongoDB database.
![database](img/er_model.drawio.png)

## Backend
This folder contains the **FastAPI** application that was used to abstract the semantic search engine
for the frontend application.
It relies on the classical REST-API structure.
```
│   
│      
│
└───models
│   
│   
└───routers
│   
│       
└───services
│
│
|   
│   main.py
```

### main.py
Contains the main entry point of the REST-API project.
Run **uvicorn main:app --reload** to start the REST-API.

### models
Contains modules that abstract the main business logic data.
This represents request bodies, response bodies and models representing chunks, papers and authors.

### routers
Represents modules that encapsulate API controllers with HTTP methods
that can be called from different client applications.
The main controllers are controllers for the semantic/lexical search in abstracts and titles.

### services
This folder contains modules that encapsulate the business logic used to communicate with the MongoDB database,
to preprocess data and to embed data.

## Frontend
This folder contains the frontend application programmed with **Gradio**.
```
│   
│      
│
└───models
│   
│       
└───services
│
│
|   
│   main.py
```

### main.py
Contains the main entry point of the frontend application.
Run **python main.py** to start the application.

### models
Contains modules that abstract the main business logic data.
These are models representing chunks, papers and authors.

### services
This folder contains modules that encapsulate the business logic used to communicate with the REST-API (backend in **FastAPI**) used to serve
the semantic engine for the application.

## System architecture
The following picture summarizes the architecture of the whole process
and system.
![system](img/system_architecture.png)

## Run the project
1. Create a MongoDB cluster. 
2. Create a .env file in the [root](./DataPreparation/) of the data preparation project 
and the [root](./Backend/) of the backend project.
3. Create the following variables in the .env files: MONGODB_URL=YOUR-CLUSTER-URL.
4. Navigate to the [data preparation project](./DataPreparation/) and execute the file **main.ipynb**.
5. Navigate to the [backend project](./Backend/) and execute the file **main.py** using **uvicorn main:app --reload**.
6. Navigate to the [frontend project](./Frontend/) and execute the file **main.py** using **python main.py**. You can change the URL
of the backend in the [config.py](./Frontend/config.py) file.
7. Navigate to the URL of the frontend application in your browser (see the terminal).

## Some screenshots
Lexical search in titles (search query: health system)
![lexical_title](img/lexical_title_1.png)
Lexical search in abstracts (search query: health system)
![lexical_abstract](img/lexical_abstract_1.png)
Semantic search in titles (search query: european healthiness system)
![semantic_title](img/semantic_title_1.png)
Semantic search in abstracts (search query: very exhausted)
![semantic_abstract](img/semantic_abstract_1.png)
from fastapi import FastAPI
from routers import titlesearch_controller
from routers import abstractsearch_controller

# Initialize the API and create routers
app = FastAPI()
app.include_router(titlesearch_controller.router)
app.include_router(abstractsearch_controller.router)

@app.get("/")
async def root():
    """The root of the application.

    Returns:
        _type_: The return message.
    """
    return {"message": "200"}

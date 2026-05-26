from pydantic import BaseModel

class BookRequest(BaseModel):
    author_id: int
    title:str
    description:str
    total_stock:int
    available_stock:int

class BooksResponse(BaseModel):
    id: int
    title: str
    description: str
    author_id: int
    author_name: str
    author_nationality:str





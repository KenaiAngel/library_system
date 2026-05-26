from pydantic import BaseModel

class BookRequest(BaseModel):
    author_id: int
    title:str
    description:str
    total_stock:int
    available_stock:int




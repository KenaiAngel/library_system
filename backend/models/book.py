from pydantic import BaseModel, model_validator, field_validator


class BookRequest(BaseModel):
    author_id: int
    title:str
    description:str
    total_stock:int
    available_stock:int

    @field_validator('title','description')
    @classmethod
    def validate_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value


    @model_validator(mode="after")
    def validate_stock(self):

        if self.author_id <= 0:
            raise ValueError("User id must be greater than 0")


        if self.total_stock < 0:
            raise ValueError("Total stock cannot be less than 0")

        if self.available_stock < 0:
            raise ValueError("Available stock cannot be less than 0")

        if self.available_stock > self.total_stock:
            raise ValueError(
                "Available stock cannot be greater than total stock"
            )

        return self

class BooksResponse(BaseModel):
    id: int
    title: str
    description: str
    author_id: int
    author_name: str
    author_nationality:str





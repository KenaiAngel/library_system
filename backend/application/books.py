from fastapi import APIRouter
from starlette import status
from models.book import BookRequest
from security.jwt import user_dependency
from security.constants import ADMIN_ROLE
from fastapi import HTTPException
from domain.books import add_book, get_books, delete_book

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookRequest, user:user_dependency):
    if user['role'] != ADMIN_ROLE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = 'Forbidden',
        )
    book = add_book(book)

    return book

@router.get("",status_code=status.HTTP_200_OK)
async def obtain_books():
    return get_books()

@router.delete("",status_code=status.HTTP_204_NO_CONTENT)
async def remove_book(book_id:int, user:user_dependency):
    if user['role'] != ADMIN_ROLE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = 'Forbidden',
        )
    delete_book(book_id)
    return




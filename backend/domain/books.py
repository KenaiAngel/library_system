from models.book import BookRequest
from database.models import Book, BookAuthor, Author

def add_book(request:BookRequest):
    new_book = Book.create(
        title=request.title,
        description=request.description,
        total_stock=request.total_stock,
        available_stock=request.available_stock,
    )
    author = Author.get_by_id(request.author_id)

    BookAuthor.create(
        book=new_book,
        author=author
    )
    return new_book

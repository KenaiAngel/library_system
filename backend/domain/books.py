from models.book import BookRequest
from database.models import Book, BookAuthor, Author

def add_book(request:BookRequest):
    author = Author.get_or_none(Author.id == request.author_id)
    if not author:
        return {'status':False,'detail':'Author not found'}
    new_book = Book.create(
        title=request.title,
        description=request.description,
        total_stock=request.total_stock,
        available_stock=request.available_stock,
    )

    BookAuthor.create(
        book=new_book,
        author=author
    )

    response_book = {
        'id': new_book.id,
        'title': new_book.title,
        'description': new_book.description,
        'total_stock': new_book.total_stock,
        'available_stock': new_book.available_stock,
        'is_active': new_book.is_active,
    }
    return {'status':True,'data':response_book}

def get_books():
    query = (
        Book
        .select(Book,Author)
        .where(Book.is_active)
        .join(BookAuthor)
        .join(Author)
        .order_by(Book.id)
        .paginate(1,20)
    )
    books= []
    for book in query:
        current_book = {
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'total_stock': book.total_stock,
            'available_stock': book.available_stock,
            'author':{
                'id': book.bookauthor.author.id,
                'name': book.bookauthor.author.name,
                'nationality': book.bookauthor.author.nationality,
            }
        }

        books.append(current_book)

    return books

def delete_book(book_id):
    book = Book.get_or_none(Book.id == book_id)
    if not book:
        return {'status':False,'detail':'Book not found'}
    book.is_active = False
    book.save(only=[Book.is_active])
    return {'status':True}

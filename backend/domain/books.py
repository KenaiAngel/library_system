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
        print (f'{book.id}, {book.bookauthor.author.name}')
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
    book = Book.get_by_id(book_id)
    book.is_active = False
    book.save(only=[Book.is_active])

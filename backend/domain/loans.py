from database.models import Loan, User, Book
from models.loan import LoanRequest

def add_new_loan(loan:LoanRequest):
    book = Book.get_or_none(Book.id == loan.book_id)
    if book is None:
        return {'status':False, 'detail':'Book not found'}

    if book.available_stock == 0:
        return {'status':False, 'detail':'No available stock'}

    user = User.get_by_id(loan.user_id)
    if user is None:
        return {'status': False, 'detail': 'User not found'}

    book.available_stock -= 1
    book.save(only=[Book.available_stock])

    new_loan = Loan.create(
        book = book,
        user = user,
        lend_date=loan.lend_date,
        expected_return_date=loan.expected_return_date,
        is_active=True,
    )
    return new_loan
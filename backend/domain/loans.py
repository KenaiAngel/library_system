from database.models import Loan, User, Book
from models.loan import LoanRequest
from datetime import timedelta

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

def extend_loan(loan_id:int,user_id:int):
    loan = Loan.get_or_none((Loan.id == loan_id) & (Loan.user_id == user_id))
    if loan is None:
        return {'status':False, 'detail':'Loan not found'}
    loan.expected_return_date += timedelta(days=10)
    loan.save(only=[Loan.expected_return_date])
    return {'status':True,'data':loan}







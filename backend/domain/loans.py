from database.models import Loan, User, Book
from models.loan import LoanRequest
from datetime import timedelta, datetime

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

    final_loan = {
        'id': new_loan.id,
        'lend_date': new_loan.lend_date,
        'expected_return_date': new_loan.expected_return_date,
        'is_active': new_loan.is_active,
        'book': {
            'id': new_loan.book.id,
            'title': new_loan.book.title,
            'description': new_loan.book.description,
            'total_stock': new_loan.book.total_stock,
            'available_stock': new_loan.book.available_stock,

        },
        'user': {
            'id': new_loan.user.id,
            'username': new_loan.user.username,
            'email': new_loan.user.email,
        }

    }
    return final_loan

def extend_loan(loan_id:int,user_id:int | None = None):
    loan = {}
    if user_id is None:
        loan = Loan.get_or_none(Loan.id == loan_id)
    else:
        loan = Loan.get_or_none((Loan.id == loan_id) & (Loan.user_id == user_id))
    if loan is None:
        return {'status':False, 'detail':'Loan not found'}
    loan.expected_return_date += timedelta(days=10)
    loan.save(only=[Loan.expected_return_date])
    return {'status':True,'data':loan}

def end_loan(loan_id:int):
    loan = Loan.get_or_none(Loan.id == loan_id)
    if loan is None:
        return {'status':False, 'detail':'Loan not found'}
    book = Book.get_or_none(Book.id == loan.book_id)

    if book is None:
        return {'status':False, 'detail':'Book not found'}

    book.available_stock += 1
    book.save(only=[Book.available_stock])

    loan.is_active = False
    loan.return_date = datetime.now()
    loan.save(only=[Loan.is_active, Loan.return_date])

    return {'status':True,'data':loan}


def get_loan(user_id: int | None = None):

    loans = []

    query = (
        Loan
        .select(Loan, User, Book)
        .join(User)
        .switch(Loan)
        .join(Book)
        .order_by(Loan.lend_date)
        .paginate(1, 20)
    )

    if user_id is not None:
        query = query.where(
            Loan.user == user_id
        )

    for loan in query:
        current_loan = {
            'id': loan.id,
            'lend_date': loan.lend_date,
            'expected_return_date': loan.expected_return_date,
            'is_active': loan.is_active,
            'book': {
                'id': loan.book.id,
                'title': loan.book.title,
                'description': loan.book.description,
                'available_stock': loan.book.available_stock,
            },
            'user': {
                'id': loan.user.id,
                'username': loan.user.username,
                'email': loan.user.email,
            },
        }

        loans.append(current_loan)

    return loans













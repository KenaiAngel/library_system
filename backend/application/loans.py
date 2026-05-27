from logging import raiseExceptions

from fastapi import APIRouter, HTTPException
from starlette import status
from security.jwt import user_dependency
from models.loan import LoanRequest
from domain.loans import add_new_loan, extend_loan, get_loan, end_loan
from security.constants import ADMIN_ROLE, READER_ROLE

router = APIRouter(
    prefix="/loans",
    tags=["loans"],
)

@router.get("",status_code=status.HTTP_200_OK)
async def obtain_loans(user: user_dependency):
    loans = []
    if user['role'] == ADMIN_ROLE:
        loans = get_loan()
    elif user['role'] == READER_ROLE:
        loans = get_loan(user['id'])
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return loans


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_loan(loan:LoanRequest, user: user_dependency):
    if user['role'] != ADMIN_ROLE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    action = add_new_loan(loan)
    return action

@router.put("/{loan_id}",status_code=status.HTTP_202_ACCEPTED)
async def edit_loan(loan_id:int ,user: user_dependency):
    response= {}

    if user['role'] == ADMIN_ROLE:
        response = extend_loan(loan_id)

    elif user['role'] == READER_ROLE:
        response = extend_loan(loan_id,user['id'])
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    if not response['status']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response['detail'],
        )
    return response['data']

@router.delete("/{loan_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_loan(loan_id:int ,user: user_dependency):
    if user['role'] != ADMIN_ROLE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    loan = end_loan(loan_id)
    print(loan)






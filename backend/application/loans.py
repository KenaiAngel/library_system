from fastapi import APIRouter, HTTPException
from starlette import status
from security.jwt import user_dependency
from models.loan import LoanRequest
from domain.loans import add_new_loan, extend_loan
from security.constants import ADMIN_ROLE, READER_ROLE

router = APIRouter(
    prefix="/loans",
    tags=["loans"],
)

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
async def edit_loan(loan_id:int ,user: user_dependency, user_id:int | None = None):
    response= {}

    if user['role'] == ADMIN_ROLE:
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough parameters",
            )
        response = extend_loan(loan_id,user_id)

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


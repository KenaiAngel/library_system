from fastapi import APIRouter, HTTPException
from starlette import status
from security.jwt import user_dependency
from models.loan import LoanRequest
from domain.loans import add_new_loan
from security.constants import ADMIN_ROLE

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
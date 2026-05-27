from datetime import datetime, date

from pydantic import BaseModel, model_validator

class LoanRequest(BaseModel):
    book_id: int
    user_id: int
    lend_date: datetime
    expected_return_date: datetime

    @model_validator(mode="after")
    def validate_loan(self):

        if self.user_id <= 0:
            raise ValueError("User id must be greater than 0")

        if self.book_id <= 0:
            raise ValueError("Book id must be greater than 0")

        if self.return_date <= self.lend_date:
            raise ValueError(
                "Return date must be greater than lend date"
            )

        return self


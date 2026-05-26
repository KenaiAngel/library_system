from datetime import datetime

from pydantic import BaseModel

class LoanRequest(BaseModel):
    book_id: int
    user_id: int
    lend_date: datetime
    expected_return_date: datetime


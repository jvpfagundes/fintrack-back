from pydantic import BaseModel
from typing import Optional


class ExpenseCreate(BaseModel):
    amount: float
    category_id: str
    date: str
    time: str
    user_id: Optional[str] = None
    description: Optional[str] = None



class ExpenseDelete(BaseModel):
    id: str
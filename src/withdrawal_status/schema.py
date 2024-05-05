from typing import Optional
from pydantic import BaseModel


class WithdrawalStatusBase(BaseModel):
    name: str

class WithdrawalStatusRead(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    slug_name: Optional[str] = None

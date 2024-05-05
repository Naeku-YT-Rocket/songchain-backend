from typing import Optional
from pydantic import BaseModel


class WithdrawalMethodRead(BaseModel):
    id: Optional[int] = None
    name: str
    slug_name: Optional[str] = None

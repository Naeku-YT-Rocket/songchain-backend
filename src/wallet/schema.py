
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class WalletBase(BaseModel):
    pass

class WalletCreate(WalletBase):
    owner_email: str

class WalletUpdate(WalletBase):
    balance: Optional[float] = None

class WalletRead(WalletBase):
    id: UUID
    balance: Optional[float] = None
    owner_email: Optional[str] = None

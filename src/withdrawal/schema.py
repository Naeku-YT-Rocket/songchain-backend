from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from src.wallet.schema import WalletRead
from src.withdrawal_status.schema import WithdrawalStatusRead
from src.withdrawal_method.schema import WithdrawalMethodRead

class WithdrawalBase(BaseModel):
    pass

class WithdrawalCreate(WithdrawalBase):
    amount: float = Field(None, ge=10)
    wallet: WalletRead
    withdrawal_method: WithdrawalMethodRead

class WithdrawalRead(BaseModel):
    id: UUID
    amount: Optional[float] = None
    wallet: Optional[WalletRead] = None
    withdrawal_status: Optional[WithdrawalStatusRead] = None
    withdrawal_method: Optional[WithdrawalMethodRead] = None
 
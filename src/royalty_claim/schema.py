from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from src.royalty.schema import RoyaltyRead
from src.partition.schema import PartitionRead


class RoyaltyClaimBase(BaseModel):
    pass


class RoyaltyClaimCreate(RoyaltyClaimBase):
    royalty: RoyaltyRead
    partition: PartitionRead


class RoyaltyClaimRead(RoyaltyClaimBase):
    id: UUID
    is_claimed: Optional[bool] = None
    amount_to_claim: Optional[float] = None
    royalty: Optional[RoyaltyRead] = None
    partition: Optional[PartitionRead] = None

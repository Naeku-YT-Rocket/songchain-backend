from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from src.partition.schema import PartitionRead
from src.digital_asset.schema import DigitalAssetRead


class RoyaltyBase(BaseModel):
    pass


class RoyaltyCreate(RoyaltyBase):
    amount: float
    created_by: str
    digital_asset: DigitalAssetRead


class RoyaltyRead(RoyaltyBase):
    id: UUID
    amount: Optional[float] = None
    created_by: Optional[str] = None
    digital_asset: Optional[DigitalAssetRead] = None

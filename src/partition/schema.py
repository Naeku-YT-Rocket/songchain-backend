
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from src.partition_status.schema import PartitionStatusRead
from src.digital_asset.schema import DigitalAssetRead
from src.wallet.schema import WalletRead


class PartitionBase(BaseModel):
    pass


class PartitionCreate(PartitionBase):
    price: float
    wallet: WalletRead
    digital_asset: DigitalAssetRead


class PartitionRead(PartitionBase):
    id: UUID
    price: Optional[float] = None
    wallet: Optional[WalletRead] = None
    digital_asset: Optional[DigitalAssetRead] = None
    is_offered: Optional[bool] = None


class PartitionPrice(PartitionBase):
    price: float = Field(None, ge=1) 

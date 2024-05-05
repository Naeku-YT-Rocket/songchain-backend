import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from src.partition_status.schema import PartitionStatusRead
from src.partition.schema import PartitionRead
from datetime import date, datetime, time, timedelta


class PartitionEventBase(BaseModel):
    pass

class PartitionEventCreate(BaseModel):
    partition: PartitionRead
    partition_status: PartitionStatusRead

class PartitionEventRead(BaseModel):
    id: UUID
    buyer_wallet_id: Optional[UUID] = None
    seller_wallet_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    partition_status: Optional[PartitionStatusRead] = None
    partition: Optional[PartitionRead] = None

from typing import List, Optional
from uuid import UUID
from src.partition_event.schema import PartitionEventRead
from src.partition_event.service import get_all
from src.config.database import DbSession
from fastapi import APIRouter


router = APIRouter(
    prefix="/partition_event"
)


@router.get("/", tags=["partition_event"], response_model=List[PartitionEventRead])
def get_partition_events(
    db_session: DbSession,
    digital_asset_id: Optional[UUID] = None,
    limit: int = 10,
    offset: int = 0
):
    
    partitions_model = get_all(
        db_session=db_session,
        limit=limit,
        offset=offset,
        digital_asset_id=digital_asset_id
    )

    return partitions_model

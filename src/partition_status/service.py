from uuid import UUID

from fastapi import HTTPException
from src.config.database import DbSession
from src.partition_status.models import PartitionStatusModel


def get_or_raise(db_session: DbSession, partition_status_id: int) -> PartitionStatusModel:
    """Get partition status or raise exception"""

    partition_status_model = db_session.query(PartitionStatusModel).filter(PartitionStatusModel.id == partition_status_id).first()
    if not partition_status_model:
        raise HTTPException(status_code=400, detail=f"Listing status with id: '{partition_status_id}' doesn't exist")
    return partition_status_model


def get_offered_status(db_session: DbSession) -> PartitionStatusModel:
    """Get 'offered' partition status"""

    return db_session.query(PartitionStatusModel).filter(PartitionStatusModel.name == "OFFERED").first()


def get_cancelled_status(db_session: DbSession) -> PartitionStatusModel:
    """Get 'offered' partition status"""

    return db_session.query(PartitionStatusModel).filter(PartitionStatusModel.name == "CANCELLED").first()


def get_purchased_status(db_session: DbSession) -> PartitionStatusModel:
    """Get 'offered' partition status"""

    return db_session.query(PartitionStatusModel).filter(PartitionStatusModel.name == "PURCHASED").first()

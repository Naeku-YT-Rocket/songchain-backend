from typing import List
from uuid import UUID
from src.digital_asset.models import DigitalAssetModel
from src.partition_event.models import PartitionEventModel
from src.partition_status.models import PartitionStatusModel
from src.partition.models import PartitionModel
from src.config.database import DbSession


def create(
        db_session: DbSession,
        partition_model: PartitionModel,
        partition_status_model: PartitionStatusModel,
        buyer_wallet_id: UUID,
        seller_wallet_id: UUID
) -> PartitionEventModel:
    """Creates a partition event"""

    partition_event_model = PartitionEventModel(
        partition=partition_model,
        partition_status=partition_status_model,
        buyer_wallet_id=buyer_wallet_id,
        seller_wallet_id=seller_wallet_id
    )

    db_session.add(partition_event_model)
    db_session.commit()
    db_session.refresh(partition_event_model)

    return partition_event_model


def get_all(
        db_session: DbSession,
        limit: int,
        offset: int,
        digital_asset_id: UUID | None
) -> List[PartitionEventModel]:
    """Gets all partition events"""

    query = db_session.query(PartitionEventModel)

    if digital_asset_id:
        query = query.join(PartitionModel).join(DigitalAssetModel).filter(DigitalAssetModel.id == digital_asset_id)

    return query.limit(limit).offset(offset).all()

from typing import List
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import and_, func
from src.partition_status.models import PartitionStatusModel
from src.partition.models import PartitionModel
from src.digital_asset.models import DigitalAssetModel
from src.digital_asset.schema import DigitalAssetCreate
from src.partition_event.models import PartitionEventModel
from src.config.database import DbSession


def create(db_session: DbSession, digital_asset_input: DigitalAssetCreate) -> DigitalAssetModel:
    """Creates a digital asset"""

    digital_asset_model = DigitalAssetModel(
        name=digital_asset_input.name,
        owner_email=digital_asset_input.owner_email,
        cover_art_uri=digital_asset_input.cover_art_uri,
        artist_name=digital_asset_input.artist_name,
        available_partitions=digital_asset_input.available_partitions
    )

    db_session.add(digital_asset_model)
    db_session.commit()
    db_session.refresh(digital_asset_model)

    return digital_asset_model


def get_all(db_session: DbSession, limit: int, offset: int) -> List[DigitalAssetModel]:
    """Get all digital assets"""

    return db_session.query(DigitalAssetModel).limit(limit).offset(offset).all()


def get_or_raise(db_session: DbSession, digital_asset_id: UUID) -> DigitalAssetModel:
    """Get digital asset or raise exception"""

    digital_asset_model = db_session.query(DigitalAssetModel).filter(DigitalAssetModel.id == digital_asset_id).first()
    if not digital_asset_model:
        raise HTTPException(status_code=400, detail=f"Digital asset with id: '{digital_asset_id}' doesn't exist")
    return digital_asset_model


def delete(db_session: DbSession, digital_asset_id: UUID) -> UUID:
    """Deletes a digital asset"""

    digital_asset_model = get_or_raise(db_session=db_session, digital_asset_id=digital_asset_id)

    db_session.delete(digital_asset_model)
    db_session.commit()

    return digital_asset_id


def compute_floor_price(db_session: DbSession, digital_asset_id: UUID) -> float:
    """Computes digital asset floor price"""

    get_or_raise(db_session=db_session, digital_asset_id=digital_asset_id)

    floor_price = db_session.query(func.min(PartitionModel.price)).join(DigitalAssetModel).filter(
        DigitalAssetModel.id == digital_asset_id, 
        PartitionModel.is_offered.is_(True)
    ).scalar() or 0

    return floor_price


def compute_offering_rate(db_session: DbSession, digital_asset_id: UUID) -> float:
    """Compute digital asset offered pct"""

    get_or_raise(db_session=db_session, digital_asset_id=digital_asset_id)

    total_partitions_count = db_session.query(PartitionModel).join(DigitalAssetModel).filter(DigitalAssetModel.id == digital_asset_id).count()

    offered_partitions_count = db_session.query(PartitionModel).join(DigitalAssetModel).filter(DigitalAssetModel.id == digital_asset_id, PartitionModel.is_offered.is_(True)).count()

    offering_rate = offered_partitions_count / total_partitions_count

    return offering_rate


def compute_total_sales(db_session: DbSession, digital_asset_id: UUID) -> float:
    """Compute digital asset total sales"""

    get_or_raise(db_session=db_session, digital_asset_id=digital_asset_id)

    total_sales = (db_session.query(PartitionEventModel)
                   .join(PartitionModel)
                   .join(DigitalAssetModel)
                   .join(PartitionStatusModel)
                   .filter(
                       DigitalAssetModel.id == digital_asset_id,
                       PartitionStatusModel.name == "PURCHASED"
                    )).count()

    return total_sales

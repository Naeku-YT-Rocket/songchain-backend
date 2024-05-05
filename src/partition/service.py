from typing import List
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import func
from src.partition.models import PartitionModel
from src.partition.schema import PartitionCreate, PartitionRead
from src.config.database import DbSession
from src.digital_asset import service as digital_asset_service
from src.wallet import service as wallet_service
from src.wallet.models import WalletModel
from src.partition_status import service as partition_status_service
from src.partition_event import service as partition_event_service
from src.digital_asset.models import DigitalAssetModel


def create(db_session: DbSession, partition_input: PartitionCreate) -> PartitionRead:
    """Creates a partition"""

    digital_asset_model = digital_asset_service.get_or_raise(db_session=db_session, digital_asset_id=partition_input.digital_asset.id) # type: ignore

    partitions_model = get_by_digital_asset_or_none(db_session=db_session, digital_asset_id=partition_input.digital_asset.id) # type: ignore

    max_partitions_reached = len(partitions_model) >= digital_asset_model.available_partitions

    if max_partitions_reached: # type: ignore
        raise HTTPException(status_code=400, detail=f"Max partitions reached for digital asset with id: {partition_input.digital_asset.id}")
    
    wallet_model = wallet_service.get_or_raise(db_session=db_session, wallet_id=partition_input.wallet.id) # type: ignore

    partition_model = PartitionModel(
        wallet=wallet_model,
        digital_asset=digital_asset_model,
        price=partition_input.price
    )

    db_session.add(partition_model)
    db_session.commit()
    db_session.refresh(partition_model)

    return partition_model


def update_price(db_session: DbSession, partition_id: UUID, price: float) -> PartitionModel:
    """Update partition price"""

    partition_model = get_or_raise(db_session=db_session, partition_id=partition_id)

    if partition_model.is_offered: # type: ignore
        raise HTTPException(status_code=400, detail="Can't update a partition price while it's offered")

    setattr(partition_model, "price", price)

    db_session.add(partition_model)
    db_session.commit()
    db_session.refresh(partition_model)

    return partition_model


def get_by_digital_asset_or_none(db_session: DbSession, digital_asset_id: UUID) -> List[PartitionModel]:
    """Get all partitions by digital asset"""

    return db_session.query(PartitionModel).filter(PartitionModel.digital_asset_id == digital_asset_id).all()


def get_all(
        db_session: DbSession,
        limit: int,
        offset: int,
        owner_email: str | None,
        wallet_id: UUID | None,
        digital_asset_id: UUID | None,
        is_offered: bool | None,
        artist_name: str | None,
        product_name: str | None,
        excluded_wallet_id: UUID | None
) -> List[PartitionModel]:
    """Get all partitions"""

    query = db_session.query(PartitionModel)

    if owner_email:
        query = query.join(WalletModel).filter(WalletModel.owner_email == owner_email)

    if artist_name and product_name:
        query = query.join(DigitalAssetModel).filter(
            DigitalAssetModel.artist_name.contains(artist_name),
            DigitalAssetModel.name.contains(product_name)
        )
    elif artist_name:
        query = query.join(DigitalAssetModel).filter(DigitalAssetModel.artist_name.contains(artist_name))
    elif product_name:
        query = query.join(DigitalAssetModel).filter(DigitalAssetModel.name.contains(product_name))

    if is_offered or is_offered == False:
        query = query.filter(PartitionModel.is_offered == is_offered)
    if wallet_id:
        query = query.filter(PartitionModel.wallet_id == wallet_id)
    if digital_asset_id:
        query = query.filter(PartitionModel.digital_asset_id == digital_asset_id)
    if excluded_wallet_id:
        query = query.filter(PartitionModel.wallet_id != excluded_wallet_id)

    return query.limit(limit).offset(offset).all()


def get_or_raise(db_session: DbSession, partition_id: UUID) -> PartitionModel:
    """Get partition or raise exception"""

    partition_model = db_session.query(PartitionModel).filter(PartitionModel.id == partition_id).first()
    if not partition_model:
        raise HTTPException(status_code=400, detail=f"Partition with id: '{partition_id}' doesn't exist")
    return partition_model


def get_total_valuation_by_wallet(db_session: DbSession, wallet_id: UUID) -> float:

    wallet_model = wallet_service.get_or_raise(db_session=db_session, wallet_id=wallet_id)
    query = db_session.query(func.sum(PartitionModel.price).label("total_valuation")).filter(PartitionModel.wallet_id == wallet_model.id)
    total_valuation = db_session.execute(query).scalar()

    return total_valuation # type: ignore


def transfer(db_session: DbSession, partition_id: UUID, recipient_wallet_id: UUID, should_commit=False) -> PartitionModel:
    """Transfers partition property"""

    partition_model = get_or_raise(db_session=db_session, partition_id=partition_id)
    wallet_model = wallet_service.get_or_raise(db_session=db_session, wallet_id=recipient_wallet_id)

    partition_model.wallet = wallet_model
    partition_model.is_offered = False # type: ignore

    db_session.flush()

    if should_commit:

        db_session.commit()
        db_session.refresh(partition_model)

    return partition_model


def delete(db_session: DbSession, partition_id: UUID) -> UUID:
    """Deletes a partition"""

    partition_model = get_or_raise(db_session=db_session, partition_id=partition_id)

    db_session.delete(partition_model)
    db_session.commit()

    return partition_model 


def offer(db_session: DbSession, partition_id: UUID) -> PartitionModel:

    partition_model = get_or_raise(db_session=db_session, partition_id=partition_id)

    if partition_model.is_offered: # type: ignore
        raise HTTPException(status_code=400, detail="Partition already offered")
    
    setattr(partition_model, "is_offered", True)

    db_session.commit()
    db_session.refresh(partition_model)

    return partition_model


def cancel_offer(db_session: DbSession, partition_id: UUID) -> PartitionModel:
    
    partition_model = get_or_raise(db_session=db_session, partition_id=partition_id)

    if not partition_model.is_offered: # type: ignore
        raise HTTPException(status_code=400, detail="Partition isn't offered")
    
    setattr(partition_model, "is_offered", False)

    db_session.commit()
    db_session.refresh(partition_model)

    return partition_model


def purchase(db_session: DbSession, buyer_wallet_id: UUID, partition_id: UUID) -> PartitionModel:

    partition_model = get_or_raise(db_session=db_session, partition_id=partition_id)

    seller_wallet_id = partition_model.wallet.id

    if not partition_model.is_offered: # type: ignore
        raise HTTPException(status_code=400, detail=f"Partition not offered")
    
    # get balance and raise exception if balance isn't enough

    wallet_model = wallet_service.get_or_raise(db_session=db_session, wallet_id=buyer_wallet_id)

    if wallet_model.balance < partition_model.price: # type: ignore
        raise HTTPException(status_code=400, detail=f"Not enough balance")
    
    wallet_service.increase_balance(
        db_session=db_session,
        wallet_id=partition_model.wallet_id, # type: ignore
        amount=partition_model.price # type: ignore
    )

    wallet_service.decrease_balance(
        db_session=db_session,
        wallet_id=buyer_wallet_id,
        amount=partition_model.price # type: ignore
    )

    transfer(
        db_session=db_session,
        partition_id=partition_id,
        recipient_wallet_id=buyer_wallet_id
    )

    # create event
    partition_status_model = partition_status_service.get_purchased_status(db_session=db_session)

    partition_event_service.create(
        db_session=db_session,
        partition_model=partition_model,
        partition_status_model=partition_status_model,
        buyer_wallet_id=buyer_wallet_id,
        seller_wallet_id=seller_wallet_id
    )

    return partition_model
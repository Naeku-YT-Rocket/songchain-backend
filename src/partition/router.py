from typing import List, Optional
from uuid import UUID
from pydantic import Field
from src.response.schema import Response
from src.wallet.schema import WalletRead
from src.partition.schema import PartitionCreate, PartitionPrice, PartitionRead
from src.partition.service import create, get_all, purchase, offer, cancel_offer, get_total_valuation_by_wallet, update_price
from src.config.database import DbSession
from fastapi import APIRouter



router = APIRouter(
    prefix="/partition"
)


@router.post("/", tags=["partition"], response_model=PartitionRead)
def create_partition(
    db_session: DbSession,
    partition_input: PartitionCreate
):

    partition_model = create(
        db_session=db_session,
        partition_input=partition_input
    )

    return partition_model


@router.get("/", tags=["partition"], response_model=List[PartitionRead])
def get_partitions(
    db_session: DbSession,
    owner_email: Optional[str] = None,
    wallet_id: Optional[UUID] = None,
    excluded_wallet_id: Optional[UUID] = None,
    is_offered: Optional[bool] = None,
    digital_asset_id: Optional[UUID] = None,
    artist_name: Optional[str] = None,
    product_name: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    
    partitions_model = get_all(
        db_session=db_session,
        limit=limit,
        offset=offset,
        wallet_id=wallet_id,
        excluded_wallet_id=excluded_wallet_id,
        digital_asset_id=digital_asset_id,
        is_offered=is_offered,
        owner_email=owner_email,
        artist_name=artist_name,
        product_name=product_name
    )

    return partitions_model


# TODO: Allow only >0 price values
@router.post("/{partition_id}/update_price", tags=["partition"], response_model=PartitionRead)
def update_partition_price(
    db_session: DbSession,
    partition_id: UUID,
    price_input: PartitionPrice
):  
    partition_model = update_price(
        db_session=db_session,
        partition_id=partition_id,
        price=price_input.price
    )
    return partition_model


@router.post("/{partition_id}/offer", tags=["partition"], response_model=PartitionRead)
def offer_partition(
    db_session: DbSession,
    partition_id: UUID
):
    partition_model = offer(
        db_session=db_session,
        partition_id=partition_id
    )

    return partition_model


@router.post("/{partition_id}/cancel_offer", tags=["partition"], response_model=PartitionRead)
def cancel_partition_offer(
    db_session: DbSession,
    partition_id: UUID
):
    partition_model = cancel_offer(
        db_session=db_session,
        partition_id=partition_id
    )

    return partition_model


@router.post("/{partition_id}/purchase", tags=["partition"], response_model=PartitionRead)
def purchase_partition(
    db_session: DbSession,
    partition_id: UUID,
    wallet: WalletRead
):

    partition_model = purchase(
        db_session=db_session,
        buyer_wallet_id=wallet.id,
        partition_id=partition_id
    )

    return partition_model


@router.get("/{wallet_id}/total_valuation", tags=["partition"], response_model=Response)
def get_total_partition_valuation_by_wallet(
    db_session: DbSession,
    wallet_id: UUID
):
    
    total_valuation = get_total_valuation_by_wallet(
        db_session=db_session,
        wallet_id=wallet_id
    )

    response = Response()
    response.total_valuation = total_valuation

    return response

from typing import List
from uuid import UUID
from src.digital_asset.schema import DigitalAssetCreate, DigitalAssetRead
from src.digital_asset.service import create, get_all, delete, compute_floor_price, compute_total_sales, compute_offering_rate, get_or_raise
from src.config.database import DbSession
from fastapi import APIRouter


router = APIRouter(
    prefix="/digital_asset"
)


@router.post("/", tags=["digital_asset"], response_model=DigitalAssetRead)
def create_digital_asset(
    db_session: DbSession,
    digital_asset_input: DigitalAssetCreate
):
    
    new_digital_asset_model = create(db_session=db_session, digital_asset_input=digital_asset_input)
    return new_digital_asset_model


@router.get("/", tags=["digital_asset"], response_model=List[DigitalAssetRead])
def get_digital_assets(
    db_session: DbSession,
    limit: int = 10,
    offset: int = 0
):

    digital_assets_model = get_all(db_session=db_session, limit=limit, offset=offset)
    return digital_assets_model


@router.get("/{digital_asset_id}", tags=["digital_asset"], response_model=DigitalAssetRead)
def get_digital_asset(
    db_session: DbSession,
    digital_asset_id: UUID
):

    digital_asset_model = get_or_raise(db_session=db_session, digital_asset_id=digital_asset_id)
    return digital_asset_model


@router.delete("/{digital_asset_id}", tags=["digital_asset"], response_model=UUID)
def delete_digital_asset(
    db_session: DbSession,
    digital_asset_id: UUID,
):

    deleted_digital_asset_id = delete(db_session=db_session, digital_asset_id=digital_asset_id)
    return deleted_digital_asset_id


@router.get("/{digital_asset_id}/floor_price", tags=["digital_asset"], response_model=float)
def compute_digital_asset_floor_price(
    db_session: DbSession,
    digital_asset_id: UUID
):
    
    floor_price = compute_floor_price(db_session=db_session, digital_asset_id=digital_asset_id)
    return floor_price


@router.get("/{digital_asset_id}/offering_pct", tags=["digital_asset"], response_model=float)
def compute_digital_asset_offering_pct(
    db_session: DbSession,
    digital_asset_id: UUID
):
    
    offering_rate = compute_offering_rate(db_session=db_session, digital_asset_id=digital_asset_id)

    return round(offering_rate * 100, 2)


@router.get("/{digital_asset_id}/total_sales", tags=["digital_asset"], response_model=float)
def compute_digital_asset_total_sales(
    db_session: DbSession,
    digital_asset_id: UUID
):
    
    total_sales = compute_total_sales(db_session=db_session, digital_asset_id=digital_asset_id)
    return total_sales

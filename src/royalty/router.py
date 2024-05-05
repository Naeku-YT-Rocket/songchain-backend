from typing import List
from uuid import UUID
from src.royalty_claim.schema import RoyaltyClaimRead
from src.royalty.schema import RoyaltyCreate, RoyaltyRead
from src.royalty.service import create
from src.config.database import DbSession
from fastapi import APIRouter


router = APIRouter(
    prefix="/royalty"
)

@router.post("/", tags=["royalty"], response_model=RoyaltyRead)
def create_royalty(
    db_session: DbSession,
    royalty_input: RoyaltyCreate
):
    new_royalty = create(db_session=db_session, royalty_input=royalty_input)
    return new_royalty

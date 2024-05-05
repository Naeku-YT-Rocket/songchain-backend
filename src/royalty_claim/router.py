from typing import List, Optional
from uuid import UUID
from src.royalty_claim.schema import RoyaltyClaimRead
from src.royalty_claim.service import claim_by_partition, claim, claim_by_wallet, get_total_amount_to_claim_by_wallet_id_or_zero
from src.config.database import DbSession
from fastapi import APIRouter
from src.royalty_claim.service import get_all


router = APIRouter(
    prefix="/royalty_claim"
)


@router.get("/", tags=["royalty_claim"], response_model=List[RoyaltyClaimRead])
def get_royalty_claims(
    db_session: DbSession,
    wallet_id: Optional[UUID] = None,
    is_claimed: Optional[bool] = None
):
    royalty_claims_model = get_all(
        db_session=db_session,
        wallet_id=wallet_id,
        is_claimed=is_claimed
    )

    return royalty_claims_model


@router.get("/wallet/{wallet_id}/claimable_amount", response_model=float)
def get_claimable_amount_by_wallet(
    db_session: DbSession,
    wallet_id: UUID
):
    claimable_amount = get_total_amount_to_claim_by_wallet_id_or_zero(db_session=db_session, wallet_id=wallet_id)
    return claimable_amount


@router.post("/{royalty_claim_id}/claim", tags=["royalty_claim"], response_model=RoyaltyClaimRead)
def claim_royalty(
    db_session: DbSession,
    royalty_claim_id: UUID
):
    claimed_royalty = claim(db_session=db_session, royalty_claim_id=royalty_claim_id)
    return claimed_royalty


@router.post("/partition/{partition_id}/claim",  tags=["royalty_claim"], response_model=List[RoyaltyClaimRead])
def claim_royalties_by_partition(
    db_session: DbSession,
    partition_id: UUID
):
    claimed_royalties = claim_by_partition(db_session=db_session, partition_id=partition_id)
    return claimed_royalties


@router.post("/wallet/{wallet_id}/claim",  tags=["royalty_claim"], response_model=List[RoyaltyClaimRead])
def claim_royalties_by_wallet(
    db_session: DbSession,
    wallet_id: UUID
):
    claimed_royalties = claim_by_wallet(db_session=db_session, wallet_id=wallet_id)  
    return claimed_royalties

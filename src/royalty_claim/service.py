from typing import List
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import func
from src.partition.models import PartitionModel
from src.config.database import DbSession
from src.royalty_claim.models import RoyaltyClaimModel
from src.wallet import service as wallet_service
from src.partition import service as partition_service
from src.wallet.models import WalletModel


def get_all(
        db_session: DbSession,
        wallet_id: UUID | None,
        is_claimed: bool | None
) -> List[RoyaltyClaimModel]:
        
    query = db_session.query(RoyaltyClaimModel)
    
    if wallet_id:
        query = query.join(PartitionModel).filter(PartitionModel.wallet_id == wallet_id)

    if is_claimed or is_claimed == False:
        query = query.filter(RoyaltyClaimModel.is_claimed == is_claimed)
    
    return query.all()

def get_or_raise(db_session: DbSession, royalty_claim_id: UUID) -> RoyaltyClaimModel:

    royalty_claim_model = db_session.query(RoyaltyClaimModel).filter(RoyaltyClaimModel.id == royalty_claim_id).first()
    if not royalty_claim_model:
        raise HTTPException(status_code=400, detail=f"Royalty claim with id: '{royalty_claim_id}' doesn't exist")
    
    return royalty_claim_model

def get_by_partition_id_or_none(db_session: DbSession, partition_id: UUID) -> List[RoyaltyClaimModel]:

    royalty_claims_model = db_session.query(RoyaltyClaimModel).filter(RoyaltyClaimModel.partition_id == partition_id).all()
    return royalty_claims_model

def get_not_claimed_by_partition_id_or_none(db_session: DbSession, partition_id: UUID) -> List[RoyaltyClaimModel]:

    royalty_claims_model = db_session.query(RoyaltyClaimModel).filter(
        RoyaltyClaimModel.partition_id == partition_id,
        RoyaltyClaimModel.is_claimed == False
    ).all()

    return royalty_claims_model

def get_total_amount_to_claim_by_partition_id(db_session: DbSession, partition_id: UUID) -> float:
    """Get total amount to claim by partition"""

    query = db_session.query(func.sum(RoyaltyClaimModel.amount_to_claim)).filter(
        RoyaltyClaimModel.partition_id == partition_id,
        RoyaltyClaimModel.is_claimed.is_(False)
    )

    total_amount_to_claim = db_session.execute(query).scalar()
    
    return total_amount_to_claim # type: ignore


def get_total_amount_to_claim_by_wallet_id_or_zero(db_session: DbSession, wallet_id: UUID) -> float:
    """Get total amount to claim by wallet"""
        
    query = db_session.query(func.sum(RoyaltyClaimModel.amount_to_claim)).join(PartitionModel).filter(
        PartitionModel.wallet_id == wallet_id,
        RoyaltyClaimModel.is_claimed.is_(False)
    )

    total_amount_to_claim = db_session.execute(query).scalar()
    
    return total_amount_to_claim or 0


def claim(db_session: DbSession, royalty_claim_id: UUID) -> RoyaltyClaimModel:
    """Claim royalty"""

    royalty_claim_model = get_or_raise(db_session=db_session, royalty_claim_id=royalty_claim_id)

    royalty_claim_model.is_claimed = True # type: ignore

    db_session.add(royalty_claim_model)
    db_session.flush()

    partition_model = partition_service.get_or_raise(db_session=db_session, partition_id=royalty_claim_model.partition_id) # type: ignore

    wallet_service.increase_balance(
        db_session=db_session,
        wallet_id=partition_model.wallet_id, # type: ignore
        amount=royalty_claim_model.amount_to_claim # type: ignore
    )

    db_session.commit()

    return royalty_claim_model


def claim_by_partition(db_session: DbSession, partition_id: UUID) -> List[RoyaltyClaimModel]:
    """Claim available royalties"""

    partition_model = partition_service.get_or_raise(db_session=db_session, partition_id=partition_id)

    royalty_claim_models = get_not_claimed_by_partition_id_or_none(db_session=db_session, partition_id=partition_id)

    if not royalty_claim_models:

        raise HTTPException(400, f"No royalties to claim for partition_id: {partition_id}")
    
    total_amount_to_claim = get_total_amount_to_claim_by_partition_id(db_session=db_session, partition_id=partition_id)
    
    bulk_update_values = [
        {
            "id": royalty_claim_model.id,
            "is_claimed": True
        }
        for royalty_claim_model in royalty_claim_models
    ]
    
    db_session.bulk_update_mappings(RoyaltyClaimModel, bulk_update_values)

    db_session.flush()
    
    wallet_service.increase_balance(
        db_session=db_session,
        wallet_id=partition_model.wallet_id, # type: ignore
        amount=total_amount_to_claim
    )

    db_session.commit()

    return royalty_claim_models


def claim_by_wallet(db_session: DbSession, wallet_id: UUID) -> List[RoyaltyClaimModel]:
    """Claim royalties by wallet"""

    wallet_service.get_or_raise(db_session=db_session, wallet_id=wallet_id)

    royalty_claim_models = get_all(db_session=db_session, wallet_id=wallet_id, is_claimed=False)

    if not royalty_claim_models:

        raise HTTPException(400, f"No royalties to claim for wallet_id: {wallet_id}")
    
    total_amount_to_claim = get_total_amount_to_claim_by_wallet_id_or_zero(db_session=db_session, wallet_id=wallet_id)

    bulk_update_values = [
        {
            "id": royalty_claim_model.id,
            "is_claimed": True
        }
        for royalty_claim_model in royalty_claim_models
    ]
    
    db_session.bulk_update_mappings(RoyaltyClaimModel, bulk_update_values)

    db_session.flush()

    wallet_service.increase_balance(
        db_session=db_session,
        wallet_id=wallet_id, # type: ignore
        amount=total_amount_to_claim
    )

    db_session.commit()

    return royalty_claim_models


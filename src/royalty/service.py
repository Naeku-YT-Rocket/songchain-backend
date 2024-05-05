from typing import List
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import func
from src.royalty_claim.models import RoyaltyClaimModel
from src.royalty.models import RoyaltyModel
from src.royalty.schema import RoyaltyCreate
from src.config.database import DbSession
from src.digital_asset import service as digital_asset_service
from src.partition import service as partition_service


def create(db_session: DbSession, royalty_input: RoyaltyCreate):
    """Creates a royalty"""

    # Get all partitions associated with this digital asset
    partitions_model = partition_service.get_by_digital_asset_or_none(db_session=db_session, digital_asset_id=royalty_input.digital_asset.id)

    if not partitions_model:
        raise HTTPException(400, f"No partition associated with digital_asset_id: '{royalty_input.digital_asset.id}'")
        
    royalty_model = RoyaltyModel(
        created_by_email=royalty_input.created_by,
        amount=royalty_input.amount,
        digital_asset_id=royalty_input.digital_asset.id
    )

    db_session.add(royalty_model)
    db_session.flush()
    
    digital_asset_model = digital_asset_service.get_or_raise(db_session=db_session, digital_asset_id=royalty_input.digital_asset.id)

    amount_to_claim = round(royalty_input.amount / digital_asset_model.available_partitions, 2) # type: ignore

    royalty_claims_model = [
        RoyaltyClaimModel(
            royalty_id=royalty_model.id,
            partition_id=partition_model.id,
            amount_to_claim=amount_to_claim
        )

        for partition_model in partitions_model
    ]

    db_session.add_all(royalty_claims_model)

    db_session.commit()

    return royalty_model    


def get_or_raise():
    pass

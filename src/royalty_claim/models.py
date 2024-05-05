from uuid import uuid4
from sqlalchemy import Boolean, Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.base.custom_base_model import CustomBaseModel
from sqlalchemy.dialects.postgresql import UUID

class RoyaltyClaimModel(CustomBaseModel):

    __tablename__ = "royalty_claims"

    id                   = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    royalty_id           = Column(ForeignKey("royalties.id"), nullable=False)
    partition_id          = Column(ForeignKey("partitions.id"), nullable=False)
    amount_to_claim      = Column(Float, nullable=False)
    is_claimed           = Column(Boolean, nullable=False, unique=False, default=False)

    royalty              = relationship("RoyaltyModel", back_populates="royalty_claim")
    partition            = relationship("PartitionModel", back_populates="royalty_claim")

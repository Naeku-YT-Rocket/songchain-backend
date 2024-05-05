from uuid import uuid4
from sqlalchemy import Boolean, Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.base.custom_base_model import CustomBaseModel
from sqlalchemy.dialects.postgresql import UUID


class RoyaltyModel(CustomBaseModel):

    __tablename__ = "royalties"

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    amount              = Column(Float, nullable=False, default=0)
    created_by_email    = Column(String, nullable=False)
    digital_asset_id    = Column(ForeignKey("digital_assets.id"))

    digital_asset       = relationship("DigitalAssetModel", back_populates="royalty")
    royalty_claim       = relationship("RoyaltyClaimModel", back_populates="royalty")
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.base.custom_base_model import CustomBaseModel
from sqlalchemy.dialects.postgresql import UUID
from src.partition_event.models import PartitionEventModel


class PartitionModel(CustomBaseModel):

    __tablename__ = "partitions"

    id                      = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    price                   = Column(Float, nullable=False, default=0)
    is_offered              = Column(Boolean, nullable=False, default=False)

    wallet_id               = Column(ForeignKey("wallets.id", onupdate="CASCADE"), nullable=False)
    digital_asset_id        = Column(ForeignKey("digital_assets.id", onupdate="CASCADE"), nullable=False)

    wallet                  = relationship("WalletModel", back_populates="partition")
    digital_asset           = relationship("DigitalAssetModel", back_populates="partition")
    partition_event         = relationship("PartitionEventModel", back_populates="partition")
    royalty_claim           = relationship("RoyaltyClaimModel", back_populates="partition")

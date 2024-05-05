from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.base.custom_base_model import CustomBaseModel
from sqlalchemy.dialects.postgresql import UUID



class PartitionEventModel(CustomBaseModel):

    __tablename__ = "partition_events"

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)

    partition_id        = Column(ForeignKey("partitions.id"), nullable=False)
    partition_status_id = Column(ForeignKey("partition_statuses.id"), nullable=False)
    buyer_wallet_id     = Column(ForeignKey("wallets.id"), nullable=False)
    seller_wallet_id    = Column(ForeignKey("wallets.id"), nullable=False)

    partition           = relationship("PartitionModel", back_populates="partition_event")
    partition_status    = relationship("PartitionStatusModel", back_populates="partition_event")
    buyer_wallet        = relationship("WalletModel", back_populates="partition_event_buyer", foreign_keys=[buyer_wallet_id])
    seller_wallet       = relationship("WalletModel", back_populates="partition_event_seller", foreign_keys=[seller_wallet_id])

from uuid import uuid4
from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship
from src.base.custom_base_model import CustomBaseModel
from sqlalchemy.dialects.postgresql import UUID
from src.withdrawal.models import WithdrawalModel
from src.partition_event.models import PartitionEventModel


class WalletModel(CustomBaseModel):

    __tablename__ = "wallets"

    id                      = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    owner_email             = Column(String, unique=False, nullable=False)
    balance                 = Column(Float, nullable=False, default=0)

    partition               = relationship("PartitionModel", back_populates="wallet")
    withdrawal              = relationship("WithdrawalModel", back_populates="wallet")

    partition_event_buyer   = relationship("PartitionEventModel", back_populates="buyer_wallet", foreign_keys="PartitionEventModel.buyer_wallet_id")
    partition_event_seller  = relationship("PartitionEventModel", back_populates="seller_wallet", foreign_keys="PartitionEventModel.seller_wallet_id")

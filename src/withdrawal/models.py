from uuid import uuid4
from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.base.custom_base_model import CustomBaseModel
from sqlalchemy.dialects.postgresql import UUID
from src.withdrawal_method.models import WithdrawalMethodModel
from src.withdrawal_status.models import WithdrawalStatusModel
from src.blockchain_currency.models import BlockchainCurrencyModel
from src.blockchain_network.models import BlockchainNetworkModel


class WithdrawalModel(CustomBaseModel):

    __tablename__ = "withdrawals"

    id                     = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    amount                 = Column(Float, nullable=False)
    wallet_id              = Column(ForeignKey("wallets.id"), nullable=False)
    blockchain_address     = Column(String, nullable=True, unique=False)
    withdrawal_status_id   = Column(ForeignKey("withdrawal_statuses.id"), nullable=False)
    withdrawal_method_id   = Column(ForeignKey("withdrawal_methods.id"), nullable=False)
    blockchain_network_id  = Column(ForeignKey("blockchain_networks.id"), nullable=False)
    blockchain_currency_id = Column(ForeignKey("blockchain_currencies.id"), nullable=False)

    wallet                 = relationship("WalletModel", back_populates="withdrawal")
    withdrawal_status      = relationship("WithdrawalStatusModel", back_populates="withdrawal")
    withdrawal_method      = relationship("WithdrawalMethodModel", back_populates="withdrawal")
    blockchain_network     = relationship("BlockchainNetworkModel", back_populates="withdrawal")
    blockchain_currency    = relationship("BlockchainCurrencyModel", back_populates="withdrawal")

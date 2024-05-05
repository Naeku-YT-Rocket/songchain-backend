from src.base.custom_enum_model import CustomEnumModel
from sqlalchemy.orm import relationship


class BlockchainNetworkModel(CustomEnumModel):

    __tablename__ = "blockchain_networks"

    withdrawal    = relationship("WithdrawalModel", back_populates="blockchain_network")
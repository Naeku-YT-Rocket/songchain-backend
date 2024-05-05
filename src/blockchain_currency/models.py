from src.base.custom_enum_model import CustomEnumModel
from sqlalchemy.orm import relationship


class BlockchainCurrencyModel(CustomEnumModel):

    __tablename__ = "blockchain_currencies"

    withdrawal    = relationship("WithdrawalModel", back_populates="blockchain_currency")
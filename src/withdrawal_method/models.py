from src.base.custom_enum_model import CustomEnumModel
from sqlalchemy.orm import relationship


class WithdrawalMethodModel(CustomEnumModel):

    __tablename__ = "withdrawal_methods"

    withdrawal    = relationship("WithdrawalModel", back_populates="withdrawal_method")
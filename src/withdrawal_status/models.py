from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.base.custom_enum_model import CustomEnumModel


class WithdrawalStatusModel(CustomEnumModel):

    __tablename__ = "withdrawal_statuses"

    description   = Column(String, nullable=True)
    withdrawal    = relationship("WithdrawalModel", back_populates="withdrawal_status")

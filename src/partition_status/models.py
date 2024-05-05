from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.base.custom_enum_model import CustomEnumModel
from src.base.custom_base_model import CustomBaseModel
from sqlalchemy.dialects.postgresql import UUID
from src.digital_asset.models import DigitalAssetModel


class PartitionStatusModel(CustomEnumModel):

    __tablename__ = "partition_statuses"

    description   = Column(String, nullable=True)

    partition_event = relationship("PartitionEventModel", back_populates="partition_status")


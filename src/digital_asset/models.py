from uuid import uuid4
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from src.base.custom_base_model import CustomBaseModel
from sqlalchemy.dialects.postgresql import UUID
from src.partition.models import PartitionModel
from src.royalty.models import RoyaltyModel


class DigitalAssetModel(CustomBaseModel):

    __tablename__ = "digital_assets"

    id                      = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    name                    = Column(String, nullable=False)
    owner_email             = Column(String, nullable=False)
    cover_art_uri           = Column(String, nullable=False)
    artist_name             = Column(String, nullable=False)
    available_partitions    = Column(Integer, nullable=False)

    partition               = relationship("PartitionModel", back_populates="digital_asset")
    royalty                 = relationship("RoyaltyModel", back_populates="digital_asset")

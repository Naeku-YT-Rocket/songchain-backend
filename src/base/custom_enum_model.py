from sqlalchemy import Integer, Column, String
from src.base.custom_base_model import CustomBaseModel


class CustomEnumModel(CustomBaseModel):

    __abstract__ = True

    id          = Column(Integer, primary_key=True, unique=True)
    name        = Column(String, nullable=False, unique=True)
    slug_name   = Column(String, nullable=False, unique=True)



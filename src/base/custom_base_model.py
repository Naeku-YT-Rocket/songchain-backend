from sqlalchemy import Column, DateTime, func
from src.config.database import Base


class CustomBaseModel(Base):

    __abstract__ = True

    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

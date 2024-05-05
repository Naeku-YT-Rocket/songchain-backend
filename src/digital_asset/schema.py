
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class DigitalAssetBase(BaseModel):
    pass

class DigitalAssetCreate(DigitalAssetBase):
    name: str
    owner_email: str
    artist_name: str
    cover_art_uri: str
    available_partitions: int

class DigitalAssetRead(DigitalAssetBase):
    id: UUID
    name: Optional[str] = None
    artist_name: Optional[str] = None 
    owner_email: Optional[str] = None
    cover_art_uri: Optional[str] = None
    available_partitions: Optional[int] = None    
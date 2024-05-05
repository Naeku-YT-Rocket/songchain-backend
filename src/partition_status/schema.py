from typing import Optional
from pydantic import BaseModel


class PartitionStatusBase(BaseModel):
    name: str

class PartitionStatusRead(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    slug_name: Optional[str] = None

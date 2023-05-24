import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ItemsSchema(BaseModel):
    id: Optional[uuid.UUID]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    item_id: str
    title : Optional[str] = None
    description : Optional[str] = None
    is_active: Optional[bool] = None
    items_number : Optional[int] = None
    ip_address: Optional[str] = None

    

    class Config:
        orm_mode = True
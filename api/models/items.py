from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Uuid, Boolean, Text
from api.models import BaseModel


class Items(BaseModel):
    __tablename__ = "items"

    item_id = Column(String, nullable=False)
    title = Column(String(255))
    description = Column(Text)
    is_active = Column(Boolean, default=False)
    items_number = Column(Integer)
    ip_address = Column(String, nullable=True)
    

    def __repr__(self):
        return f"{self.title}"
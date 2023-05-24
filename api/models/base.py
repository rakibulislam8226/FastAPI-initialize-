from datetime import datetime
from sqlalchemy import Column, DateTime, MetaData, Uuid, Boolean
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class BaseModel(Base):
    """
    Base abstract model to inherit other models from.
    """

    __abstract__ = True

    id = Column(Uuid, primary_key=True, index=True)
    # created_by = 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        columns = ", ".join(
            [f"{k}={repr(v)}" for k, v in self.__dict__.items() if not k.startswith("_")]
        )
        return f"<{self.__class__.__name__}({columns})>"
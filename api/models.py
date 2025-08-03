from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from api.db import Base

class Memo(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(Text, nullable=False)
    status = Column(String(255), nullable=False, default='Not started')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
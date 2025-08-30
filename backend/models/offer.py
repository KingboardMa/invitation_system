from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base

class Offer(Base):
    """邀请码项目表"""
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    total_count = Column(Integer, default=0)
    remaining_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 关系
    invitation_codes = relationship("InvitationCode", back_populates="offer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Offer(name='{self.name}', title='{self.title}', remaining={self.remaining_count}/{self.total_count})>"

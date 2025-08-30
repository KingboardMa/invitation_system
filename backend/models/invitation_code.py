from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base

class InvitationCode(Base):
    """邀请码表"""
    __tablename__ = "invitation_codes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False)
    code = Column(String(255), nullable=False)
    is_used = Column(Boolean, default=False, index=True)
    used_at = Column(DateTime)
    user_ip = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # 关系
    offer = relationship("Offer", back_populates="invitation_codes")

    def __repr__(self):
        status = "已使用" if self.is_used else "未使用"
        return f"<InvitationCode(code='{self.code[:10]}...', status='{status}')>"

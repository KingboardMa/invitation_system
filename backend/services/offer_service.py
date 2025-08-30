from typing import Optional
from sqlalchemy.orm import Session
from models.offer import Offer
from models.invitation_code import InvitationCode
from sqlalchemy.sql import func

class OfferService:
    """Offer相关业务逻辑"""

    def __init__(self, db: Session):
        self.db = db

    def get_offer_by_name(self, name: str) -> Optional[Offer]:
        """根据名称获取offer"""
        return self.db.query(Offer).filter(Offer.name == name).first()

    def create_offer(self, name: str, title: str, description: str = None) -> Offer:
        """创建新的offer"""
        offer = Offer(
            name=name,
            title=title,
            description=description,
            total_count=0,
            remaining_count=0
        )
        self.db.add(offer)
        self.db.commit()
        self.db.refresh(offer)
        return offer

    def update_offer_stats(self, offer_id: int):
        """更新offer的统计信息"""
        # 获取总数和剩余数
        total_count = self.db.query(InvitationCode).filter(
            InvitationCode.offer_id == offer_id
        ).count()

        remaining_count = self.db.query(InvitationCode).filter(
            InvitationCode.offer_id == offer_id,
            InvitationCode.is_used == False
        ).count()

        # 更新offer统计
        self.db.query(Offer).filter(Offer.id == offer_id).update({
            "total_count": total_count,
            "remaining_count": remaining_count,
            "updated_at": func.now()
        })
        self.db.commit()

    def get_offer_stats(self, offer_name: str) -> dict:
        """获取offer的详细统计信息"""
        offer = self.get_offer_by_name(offer_name)
        if not offer:
            return None

        # 获取最近的申请记录（最多10条）
        recent_claims = self.db.query(InvitationCode).filter(
            InvitationCode.offer_id == offer.id,
            InvitationCode.is_used == True
        ).order_by(InvitationCode.used_at.desc()).limit(10).all()

        # 脱敏处理邀请码
        recent_claims_data = []
        for claim in recent_claims:
            code_masked = f"***{claim.code[-6:]}" if len(claim.code) > 6 else "***"
            recent_claims_data.append({
                "code": code_masked,
                "claimed_at": claim.used_at,
                "user_ip": claim.user_ip
            })

        usage_rate = offer.total_count - offer.remaining_count
        usage_rate = usage_rate / offer.total_count if offer.total_count > 0 else 0

        return {
            "total_codes": offer.total_count,
            "used_codes": offer.total_count - offer.remaining_count,
            "remaining_codes": offer.remaining_count,
            "usage_rate": round(usage_rate, 3),
            "recent_claims": recent_claims_data
        }

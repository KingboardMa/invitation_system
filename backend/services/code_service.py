from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime
from models.offer import Offer
from models.invitation_code import InvitationCode

class CodeService:
    """邀请码相关业务逻辑"""

    def __init__(self, db: Session):
        self.db = db

    def claim_code(self, offer_name: str, user_ip: str = None, user_agent: str = None) -> Optional[str]:
        """申请一个邀请码"""
        # 查找offer
        offer = self.db.query(Offer).filter(
            Offer.name == offer_name,
            Offer.is_active == True
        ).first()

        if not offer:
            raise ValueError("邀请码项目不存在或已停用")

        # 查找未使用的邀请码
        unused_code = self.db.query(InvitationCode).filter(
            InvitationCode.offer_id == offer.id,
            InvitationCode.is_used == False
        ).first()

        if not unused_code:
            raise ValueError("邀请码已用完")

        # 标记为已使用
        unused_code.is_used = True
        unused_code.used_at = datetime.now()
        unused_code.user_ip = user_ip
        unused_code.user_agent = user_agent

        # 更新offer的剩余数量
        offer.remaining_count -= 1
        offer.updated_at = datetime.now()

        self.db.commit()

        return unused_code.code

    def import_codes(self, offer_name: str, codes: List[str]) -> dict:
        """导入邀请码到指定offer"""
        # 查找或创建offer
        offer = self.db.query(Offer).filter(Offer.name == offer_name).first()
        if not offer:
            raise ValueError(f"Offer '{offer_name}' 不存在，请先创建")

        new_codes = 0
        duplicate_codes = 0

        for code in codes:
            code = code.strip()
            if not code:
                continue

            # 检查是否已存在
            existing = self.db.query(InvitationCode).filter(
                InvitationCode.offer_id == offer.id,
                InvitationCode.code == code
            ).first()

            if existing:
                duplicate_codes += 1
                continue

            # 创建新的邀请码
            invitation_code = InvitationCode(
                offer_id=offer.id,
                code=code,
                is_used=False
            )
            self.db.add(invitation_code)
            new_codes += 1

        # 提交事务
        self.db.commit()

        # 更新offer统计
        from services.offer_service import OfferService
        offer_service = OfferService(self.db)
        offer_service.update_offer_stats(offer.id)

        return {
            "new_codes": new_codes,
            "duplicate_codes": duplicate_codes,
            "total_processed": len(codes)
        }

    def get_available_count(self, offer_id: int) -> int:
        """获取可用邀请码数量"""
        return self.db.query(InvitationCode).filter(
            InvitationCode.offer_id == offer_id,
            InvitationCode.is_used == False
        ).count()

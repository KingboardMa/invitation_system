from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models.database import get_db
from services.offer_service import OfferService
from services.code_service import CodeService
from schemas import (
    OfferInfoResponse,
    ClaimRequest,
    ClaimResponse,
    StatsResponse,
    ErrorResponse
)
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/offers", tags=["offers"])

@router.get("/{offer_name}/info", response_model=OfferInfoResponse)
async def get_offer_info(
    offer_name: str,
    db: Session = Depends(get_db)
):
    """获取offer信息"""
    try:
        # 验证offer_name不为空
        if not offer_name or offer_name.strip() == "":
            raise HTTPException(status_code=400, detail="Offer名称不能为空")

        offer_service = OfferService(db)
        offer = offer_service.get_offer_by_name(offer_name.strip())

        if not offer:
            raise HTTPException(status_code=404, detail="邀请码项目不存在")

        # 构建OfferInfo对象
        offer_info = {
            "name": offer.name,
            "title": offer.title,
            "description": offer.description,
            "total_count": offer.total_count,
            "remaining_count": offer.remaining_count,
            "is_active": offer.is_active
        }

        return OfferInfoResponse(data=offer_info)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取offer信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail="服务器内部错误")

@router.post("/{offer_name}/claim", response_model=ClaimResponse)
async def claim_invitation_code(
    offer_name: str,
    request: Request,
    claim_request: ClaimRequest = None,
    db: Session = Depends(get_db)
):
    """申请邀请码"""
    try:
        # 验证offer_name不为空
        if not offer_name or offer_name.strip() == "":
            raise HTTPException(status_code=400, detail="Offer名称不能为空")

        # 获取客户端信息
        user_ip = claim_request.user_ip if claim_request else None
        if not user_ip:
            user_ip = request.client.host

        user_agent = claim_request.user_agent if claim_request else None
        if not user_agent:
            user_agent = request.headers.get("user-agent", "")

        # 申请邀请码
        code_service = CodeService(db)
        code = code_service.claim_code(offer_name.strip(), user_ip, user_agent)

        logger.info(f"邀请码申请成功: offer={offer_name}, ip={user_ip}")

        return ClaimResponse(data={
            "code": code,
            "message": "邀请码获取成功"
        })

    except ValueError as e:
        error_msg = str(e)
        error_code = "NO_CODES_AVAILABLE" if "已用完" in error_msg else "INVALID_OFFER"
        logger.warning(f"邀请码申请失败: offer={offer_name}, error={error_msg}")
        raise HTTPException(status_code=400, detail={"error": error_msg, "error_code": error_code})

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"申请邀请码时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail="服务器内部错误")

@router.get("/{offer_name}/stats", response_model=StatsResponse)
async def get_offer_stats(
    offer_name: str,
    db: Session = Depends(get_db)
):
    """获取offer统计信息（管理员接口）"""
    try:
        # 验证offer_name不为空
        if not offer_name or offer_name.strip() == "":
            raise HTTPException(status_code=400, detail="Offer名称不能为空")

        offer_service = OfferService(db)
        stats = offer_service.get_offer_stats(offer_name.strip())

        if not stats:
            raise HTTPException(status_code=404, detail="邀请码项目不存在")

        return StatsResponse(data=stats)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取统计信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail="服务器内部错误")

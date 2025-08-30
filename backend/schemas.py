from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# 响应基础模型
class BaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None

class ErrorResponse(BaseResponse):
    success: bool = False
    error: str
    error_code: Optional[str] = None

# Offer相关模型
class OfferInfo(BaseModel):
    name: str
    title: str
    description: Optional[str]
    total_count: int
    remaining_count: int
    is_active: bool

    class Config:
        from_attributes = True

class OfferInfoResponse(BaseResponse):
    success: bool = True
    data: OfferInfo

# 邀请码申请相关模型
class ClaimRequest(BaseModel):
    user_ip: Optional[str] = None
    user_agent: Optional[str] = None

class ClaimData(BaseModel):
    code: str
    message: str

class ClaimResponse(BaseResponse):
    success: bool = True
    data: ClaimData

# 统计信息相关模型
class RecentClaim(BaseModel):
    code: str  # 脱敏后的邀请码
    claimed_at: datetime
    user_ip: str

    class Config:
        from_attributes = True

class StatsData(BaseModel):
    total_codes: int
    used_codes: int
    remaining_codes: int
    usage_rate: float
    recent_claims: List[RecentClaim] = []

class StatsResponse(BaseResponse):
    success: bool = True
    data: StatsData

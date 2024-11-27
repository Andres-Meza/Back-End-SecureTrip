from pydantic import BaseModel
from typing import Optional
from datetime import date


class PromotionBase(BaseModel):
    Description: str
    Discount: float
    StartDate: date
    EndDate: date


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    Description: Optional[str] = None
    Discount: Optional[float] = None
    StartDate: Optional[date] = None
    EndDate: Optional[date] = None


class PromotionResponse(PromotionBase):
    PromotionID: int

    class Config:
        orm_mode = True

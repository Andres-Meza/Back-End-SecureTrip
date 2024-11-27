from pydantic import BaseModel
from typing import Optional
from datetime import date


class TravelPlanBase(BaseModel):
    ClientID: int
    GuideID: int
    PhotographerID: int
    TransportID: int
    CountryID: int
    StartDate: date
    EndDate: date


class TravelPlanCreate(TravelPlanBase):
    pass


class TravelPlanUpdate(BaseModel):
    GuideID: Optional[int] = None
    PhotographerID: Optional[int] = None
    TransportID: Optional[int] = None
    CountryID: Optional[int] = None
    StartDate: Optional[date] = None
    EndDate: Optional[date] = None


class TravelPlanResponse(TravelPlanBase):
    TravelPlanID: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ServiceBase(BaseModel):
    NameService: str
    Description: str
    Price: float
    TypeService: str
    AvailabilityStatus: Optional[str] = "Disponible"
    ServicePriority: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    Description: Optional[str] = None
    Price: Optional[float] = None
    AvailabilityStatus: Optional[str] = None
    ServicePriority: Optional[str] = None


class ServiceResponse(ServiceBase):
    ServiceID: int
    LastModifiedDate: datetime

    class Config:
        orm_mode = True

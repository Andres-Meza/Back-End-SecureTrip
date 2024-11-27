from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ServiceBase(BaseModel):
    ServiceName: str
    Description: str
    Price: float
    ServiceType: str
    AvailabilityStatus: Optional[str] = "Disponible"
    ServicePriority: Optional[str] = None
    LastModified: datetime


class ServiceCreate(ServiceBase):
    ServiceName: str
    Description: str
    Price: float
    ServiceType: str
    AvailabilityStatus: str = 'Disponible'
    ServicePriority: str
    LastModified: datetime = datetime.now()


class ServiceUpdate(BaseModel):
    Description: Optional[str] = None
    Price: Optional[float] = None
    AvailabilityStatus: Optional[str] = None
    ServicePriority: Optional[str] = None


class ServiceResponse(ServiceBase):
    ServiceID: int
    LastModified: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional


class TransportServiceBase(BaseModel):
    TransportType: str
    Capacity: int
    DriverID: Optional[int] = None


class TransportServiceCreate(TransportServiceBase):
    pass


class TransportServiceUpdate(BaseModel):
    Capacity: Optional[int] = None
    DriverID: Optional[int] = None


class TransportServiceResponse(TransportServiceBase):
    TransportID: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional


class PaymentBase(BaseModel):
    ClientID: int
    ServiceID: int
    Amount: float
    PaymentMethod: str
    IPAddress: str
    Reference: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    Status: Optional[str] = "Processed"


class PaymentResponse(PaymentBase):
    PaymentID: int

    class Config:
        orm_mode = True

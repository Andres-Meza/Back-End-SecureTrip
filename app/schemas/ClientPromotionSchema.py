from pydantic import BaseModel


class ClientPromotionBase(BaseModel):
    ClientID: int
    PromotionID: int


class ClientPromotionCreate(ClientPromotionBase):
    pass


class ClientPromotionResponse(ClientPromotionBase):
    class Config:
        orm_mode = True

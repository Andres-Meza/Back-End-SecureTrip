from pydantic import BaseModel


class ServiceTravelPlanBase(BaseModel):
    ServiceID: int
    TravelPlanID: int


class ServiceTravelPlanCreate(ServiceTravelPlanBase):
    pass


class ServiceTravelPlanResponse(ServiceTravelPlanBase):
    class Config:
        orm_mode = True

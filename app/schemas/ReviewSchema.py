from pydantic import BaseModel
from typing import Optional


class ReviewBase(BaseModel):
    ClientID: int
    ServiceID: int
    Rating: int
    Comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    Rating: Optional[int] = None
    Comment: Optional[str] = None


class ReviewResponse(ReviewBase):
    ReviewID: int

    class Config:
        orm_mode = True

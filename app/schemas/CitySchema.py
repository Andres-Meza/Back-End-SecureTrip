from pydantic import BaseModel
from typing import Optional


class CityBase(BaseModel):
    NameCity: str
    CountryID: int


class CityCreate(CityBase):
    NameCity: str
    CountryID: int


class CityUpdate(BaseModel):
    NameCity: str
    CountryID: int


class CityResponse(CityBase):
    CityID: int

    class Config:
        orm_mode = True

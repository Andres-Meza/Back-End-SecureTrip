from pydantic import BaseModel
from typing import Optional


class CountryBase(BaseModel):
    NameCountry: str


class CountryCreate(CountryBase):
    NameCountry: str


class CountryUpdate(BaseModel):
    NameCountry: Optional[str] = None


class CountryResponse(CountryBase):
    CountryID: int

    class Config:
        orm_mode = True

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class ClientBase(BaseModel):
    FirstName: str
    LastName: str
    Email: str
    Password: str
    CountryID: int
    CityID: int
    LanguageID: int
    BirthDate: date
    ClientStatus: Optional[str] = "Activo"


class ClientCreate(ClientBase):
    FirstName: str
    LastName: str
    Email: EmailStr
    Password: str
    CountryID: int
    CityID: int
    LanguageID: int
    BirthDate: date


class ClientUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Email: Optional[str] = None
    Password: Optional[str] = None
    CountryID: Optional[int] = None
    CityID: Optional[int] = None
    LanguageID: Optional[int] = None
    BirthDate: Optional[date] = None
    Status: Optional[str] = None


class ClientResponse(ClientBase):
    ClientID: int

    class Config:
        orm_mode = True

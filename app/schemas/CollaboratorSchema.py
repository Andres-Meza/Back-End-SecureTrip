from pydantic import BaseModel
from typing import Optional


class CollaboratorBase(BaseModel):
    FirstName: str
    LastName: str
    Email: str
    TypeCollaborator: str
    CountryID: int
    CityID: int
    LanguageID: int
    Specialty: str
    CompetencyLevel: str
    LicenseType: str
    StatusCollaborator: Optional[str] = "Activo"


class CollaboratorCreate(CollaboratorBase):
    pass


class CollaboratorUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Email: Optional[str] = None
    TypeCollaborator: Optional[str] = None
    CountryID: Optional[int] = None
    CityID: Optional[int] = None
    LanguageID: Optional[int] = None
    Specialty: Optional[str] = None
    CompetencyLevel: Optional[str] = None
    LicenseType: Optional[str] = None
    StatusCollaborator: Optional[str] = None


class CollaboratorResponse(CollaboratorBase):
    CollaboratorID: int

    class Config:
        orm_mode = True
        alias = {
            "CompetencyLevel": "CompetencyLevel"
        }

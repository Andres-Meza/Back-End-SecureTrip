from pydantic import BaseModel
from typing import Optional

class LanguageBase(BaseModel):
		NameLanguage: str

class LanguageCreate(LanguageBase):
		pass

class LanguageUpdate(BaseModel):
		NameLanguage: Optional[str] = None

class LanguageResponse(LanguageBase):
		LanguageID: int

		class Config:
				orm_mode = True

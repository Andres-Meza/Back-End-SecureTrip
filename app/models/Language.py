from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Language(Base):
    __tablename__ = "Language"

    LanguageID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    NameLanguage = Column(
        String(50),
        unique=True,
        nullable=False
    )

    collaborators = relationship("Collaborator", back_populates="language")
    clients = relationship("Client", back_populates="language")

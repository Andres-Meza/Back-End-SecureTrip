from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Collaborator(Base):
    __tablename__ = "Collaborator"

    CollaboratorID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    FirstName = Column(
        String(100),
        nullable=False
    )

    LastName = Column(
        String(100),
        nullable=False
    )

    Email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    TypeCollaborator = Column(
        String(50),
        nullable=False
    )

    CountryID = Column(
        Integer,
        ForeignKey("Country.CountryID"),
        nullable=False
    )

    CityID = Column(
        Integer,
        ForeignKey("City.CityID"),
        nullable=False
    )

    LanguageID = Column(
        Integer,
        ForeignKey("Language.LanguageID"),
        nullable=False
    )

    Specialty = Column(
        String(100)
    )

    CompetencyLevel = Column(
        String(50)
    )

    LicenseType = Column(
        String(50)
    )

    StatusCollaborator = Column(
        String(20),
        default="Active"
    )

    # Relationships
    country = relationship("Country", back_populates="collaborators")
    city = relationship("City", back_populates="collaborators")
    language = relationship("Language", back_populates="collaborators")
    transport_services = relationship(
        "TransportService", back_populates="driver")

from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class TravelPlanning(Base):
    __tablename__ = "TravelPlanning"

    PlanningID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ClientID = Column(
        Integer,
        ForeignKey("Client.ClientID"),
        nullable=False
    )

    GuideID = Column(
        Integer,
        ForeignKey("Collaborator.CollaboratorID"),
        nullable=True
    )

    PhotographerID = Column(
        Integer,
        ForeignKey("Collaborator.CollaboratorID"),
        nullable=True
    )

    TransportID = Column(
        Integer,
        ForeignKey("TransportService.TransportID"),
        nullable=True
    )

    CountryID = Column(
        Integer,
        ForeignKey("Country.CountryID"),
        nullable=False
    )

    StartDate = Column(
        Date,
        nullable=False
    )

    EndDate = Column(
        Date,
        nullable=False
    )

    # Relationships
    client = relationship("Client", back_populates="travel_plans")
    guide = relationship("Collaborator", foreign_keys=[GuideID])
    photographer = relationship("Collaborator", foreign_keys=[PhotographerID])
    transport = relationship("TransportService", back_populates="travel_plans")
    country = relationship("Country", back_populates="travel_plans")
    services = relationship(
        "Service",
        secondary="ServicePlanning",
        back_populates="travel_plannings"
    )

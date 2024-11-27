from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class TransportService(Base):
    __tablename__ = "TransportService"

    TransportID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    TransportType = Column(
        String(50),
        nullable=False
    )

    Capacity = Column(
        Integer,
        nullable=False
    )

    DriverID = Column(
        Integer,
        ForeignKey("Collaborator.CollaboratorID"),
        nullable=False
    )

    # Relationship
    driver = relationship("Collaborator", back_populates="transport_services")
    travel_plans = relationship("TravelPlanning", back_populates="transport")

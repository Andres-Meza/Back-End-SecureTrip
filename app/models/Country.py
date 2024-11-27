from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Country(Base):
    __tablename__ = "Country"

    CountryID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    NameCountry = Column(
        String(100),
        unique=True,
        nullable=False
    )

    cities = relationship("City", back_populates="country")
    collaborators = relationship("Collaborator", back_populates="country")
    clients = relationship("Client", back_populates="country")
    travel_plans = relationship("TravelPlanning", back_populates="country")

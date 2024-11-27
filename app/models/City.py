from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class City(Base):
    __tablename__ = "City"

    CityID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    NameCity = Column(
        String(100),
        nullable=False
    )

    CountryID = Column(
        Integer,
        ForeignKey("Country.CountryID"),
        nullable=False
    )

    country = relationship("Country", back_populates="cities")
    collaborators = relationship("Collaborator", back_populates="city")
    clients = relationship("Client", back_populates="city")

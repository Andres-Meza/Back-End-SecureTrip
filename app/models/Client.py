from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Client(Base):
    __tablename__ = "Client"

    ClientID = Column(
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

    Password = Column(
        String(255),
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

    BirthDate = Column(
        Date,
        nullable=False
    )

    ClientStatus = Column(
        String(20),
        default="Activo"
    )

    LastLogin = Column(
        DateTime
    )

    FailedAttempts = Column(
        Integer,
        default=0
    )

    # Relationships
    country = relationship("Country", back_populates="clients")
    city = relationship("City", back_populates="clients")
    language = relationship("Language", back_populates="clients")
    travel_plans = relationship("TravelPlanning", back_populates="client")
    reviews = relationship("Review", back_populates="client")
    payments = relationship("Payment", back_populates="client")
    promotions = relationship(
        "Promotion",
        secondary="ClientPromotion",
        back_populates="clients"
    )

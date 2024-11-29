from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL, func
from sqlalchemy.orm import relationship
from app.database import Base


class Service(Base):
    __tablename__ = "Service"

    ServiceID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ServiceName = Column(
        String(100),
        nullable=False
    )

    Description = Column(
        Text,
        nullable=True
    )

    Price = Column(
        DECIMAL(10, 2),
        nullable=False
    )

    ServiceType = Column(
        String(50),
        nullable=False
    )

    AvailabilityStatus = Column(
        String(20),
        default="Activo"
    )

    Priority = Column(
        String(20)
    )

    LastModified = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    # Relationships
    reviews = relationship("Review", back_populates="service")
    payments = relationship("Payment", back_populates="service")
    reviews = relationship("Review", back_populates="service")
    payments = relationship("Payment", back_populates="service")
    travel_plannings = relationship(
        "TravelPlanning",
        secondary="ServicePlanning",
        back_populates="services"
    )

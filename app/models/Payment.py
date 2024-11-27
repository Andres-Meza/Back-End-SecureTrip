from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Payment(Base):
    __tablename__ = "Payment"

    PaymentID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ClientID = Column(
        Integer,
        ForeignKey("Client.ClientID"),
        nullable=False
    )

    ServiceID = Column(
        Integer,
        ForeignKey("Service.ServiceID"),
        nullable=False
    )

    Amount = Column(
        DECIMAL(10, 2),
        nullable=False
    )

    PaymentDate = Column(
        DateTime,
        nullable=False
    )

    PaymentMethod = Column(
        String(50),
        nullable=False
    )

    Status = Column(
        String(20),
        default="Processed"
    )

    IPAddress = Column(
        String(45),
        nullable=True
    )

    Reference = Column(
        String(100),
        unique=True,
        nullable=False
    )

    # Relationships
    client = relationship("Client", back_populates="payments")
    service = relationship("Service", back_populates="payments")

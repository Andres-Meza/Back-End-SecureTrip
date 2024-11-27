from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Promotion(Base):
    __tablename__ = "Promotion"

    PromotionID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    Description = Column(
        Text,
        nullable=False
    )

    Discount = Column(
        Integer,  # Representa el descuento en porcentaje
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

    # Relación con Client
    clients = relationship(
        "Client",
        secondary="ClientPromotion",
        back_populates="promotions"
    )

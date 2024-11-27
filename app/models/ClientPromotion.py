from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class ClientPromotion(Base):
    __tablename__ = "ClientPromotion"

    ClientID = Column(
        Integer,
        ForeignKey("Client.ClientID"),
        primary_key=True,
    )

    PromotionID = Column(
        Integer,
        ForeignKey("Promotion.PromotionID"),
        primary_key=True,
    )

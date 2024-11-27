from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Review(Base):
		__tablename__ = "Review"

		ReviewID = Column(
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

		Rating = Column(
				Integer,
				nullable=False
		)

		Comment = Column(
				Text,
				nullable=True
		)

		# Relationships
		client = relationship("Client", back_populates="reviews")
		service = relationship("Service", back_populates="reviews")

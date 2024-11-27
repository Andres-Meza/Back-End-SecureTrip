from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class ServicePlanning(Base):
		__tablename__ = "ServicePlanning"

		ServiceID = Column(
				Integer,
				ForeignKey("Service.ServiceID"),
				primary_key=True,
		)

		PlanningID = Column(
				Integer,
				ForeignKey("TravelPlanning.PlanningID"),
				primary_key=True,
		)

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import ServicePlanning
from app.schemas.ServicePlanningSchema import ServiceTravelPlanCreate, ServiceTravelPlanResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ServiceTravelPlanResponse)
def create_service_travel_plan(service_travel_plan: ServiceTravelPlanCreate, db: Session = Depends(get_db)):
    new_service_travel_plan = ServicePlanning(
        ServiceID=service_travel_plan.ServiceID,
        TravelPlanID=service_travel_plan.TravelPlanID
    )
    db.add(new_service_travel_plan)
    db.commit()
    db.refresh(new_service_travel_plan)
    return new_service_travel_plan


@router.get("/", response_model=list[ServiceTravelPlanResponse])
def get_service_travel_plans(db: Session = Depends(get_db)):
    return db.query(ServicePlanning).all()


@router.get("/{travel_plan_id}", response_model=list[ServiceTravelPlanResponse])
def get_service_travel_plans_by_travel_plan(travel_plan_id: int, db: Session = Depends(get_db)):
    service_travel_plans = db.query(ServicePlanning).filter(
        ServicePlanning.TravelPlanID == travel_plan_id).all()
    if not service_travel_plans:
        raise HTTPException(
            status_code=404, detail="No se encontraron servicios para esta planificación.")
    return service_travel_plans

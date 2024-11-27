from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import TravelPlanning
from app.schemas.TravelPlanSchema import TravelPlanCreate, TravelPlanUpdate, TravelPlanResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TravelPlanResponse)
def create_travel_plan(travel_plan: TravelPlanCreate, db: Session = Depends(get_db)):
    new_plan = TravelPlanning(
        ClientID=travel_plan.ClientID,
        GuideID=travel_plan.GuideID,
        PhotographerID=travel_plan.PhotographerID,
        TransportID=travel_plan.TransportID,
        CountryID=travel_plan.CountryID,
        StartDate=travel_plan.StartDate,
        EndDate=travel_plan.EndDate,
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan


@router.get("/", response_model=list[TravelPlanResponse])
def get_travel_plans(db: Session = Depends(get_db)):
    return db.query(TravelPlanning).all()


@router.get("/{travel_plan_id}", response_model=TravelPlanResponse)
def get_travel_plan(travel_plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(TravelPlanning).filter(
        TravelPlanning.TravelPlanID == travel_plan_id).first()
    if plan is None:
        raise HTTPException(
            status_code=404, detail="Planificación no encontrada")
    return plan


@router.put("/{travel_plan_id}", response_model=TravelPlanResponse)
def update_travel_plan(travel_plan_id: int, travel_plan: TravelPlanUpdate, db: Session = Depends(get_db)):
    db_plan = db.query(TravelPlanning).filter(
        TravelPlanning.TravelPlanID == travel_plan_id).first()
    if db_plan is None:
        raise HTTPException(
            status_code=404, detail="Planificación no encontrada")

    db_plan.GuideID = travel_plan.GuideID or db_plan.GuideID
    db_plan.PhotographerID = travel_plan.PhotographerID or db_plan.PhotographerID
    db_plan.TransportID = travel_plan.TransportID or db_plan.TransportID

    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.delete("/{travel_plan_id}")
def delete_travel_plan(travel_plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(TravelPlanning).filter(
        TravelPlanning.TravelPlanID == travel_plan_id).first()
    if db_plan is None:
        raise HTTPException(
            status_code=404, detail="Planificación no encontrada")

    db.delete(db_plan)
    db.commit()
    return {"message": f"Planificación {travel_plan_id} eliminada"}

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Service
from app.schemas.ServiceSchema import ServiceCreate, ServiceUpdate, ServiceResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ServiceResponse)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    new_service = Service(
        ServiceName=service.ServiceName,
        Description=service.Description,
        Price=service.Price,
        ServiceType=service.ServiceType,
        AvailabilityStatus=service.AvailabilityStatus,
        Priority=service.ServicePriority,
        LastModified=service.LastModified
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


@router.get("/", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.ServiceID == service_id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return service


@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: int, service: ServiceUpdate, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(
        Service.ServiceID == service_id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    if service.Description is not None:
        db_service.Description = service.Description
    if service.Price is not None:
        db_service.Price = service.Price
    if service.AvailabilityStatus is not None:
        db_service.AvailabilityStatus = service.AvailabilityStatus
    if service.ServicePriority is not None:
        db_service.ServicePriority = service.ServicePriority

    db.commit()
    db.refresh(db_service)
    return db_service


@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(
        Service.ServiceID == service_id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    db.delete(db_service)
    db.commit()
    return {"message": f"Servicio {service_id} eliminado"}

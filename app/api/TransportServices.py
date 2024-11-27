from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import TransportService
from app.schemas.TransportServiceSchema import TransportServiceCreate, TransportServiceUpdate, TransportServiceResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TransportServiceResponse)
def create_transport_service(transport_service: TransportServiceCreate, db: Session = Depends(get_db)):
    new_transport_service = TransportService(
        TransportType=transport_service.TransportType,
        Capacity=transport_service.Capacity,
        DriverID=transport_service.DriverID,
    )
    db.add(new_transport_service)
    db.commit()
    db.refresh(new_transport_service)
    return new_transport_service


@router.get("/", response_model=list[TransportServiceResponse])
def get_transport_services(db: Session = Depends(get_db)):
    return db.query(TransportService).all()


@router.get("/{transport_id}", response_model=TransportServiceResponse)
def get_transport_service(transport_id: int, db: Session = Depends(get_db)):
    transport_service = db.query(TransportService).filter(
        TransportService.TransportID == transport_id).first()
    if transport_service is None:
        raise HTTPException(
            status_code=404, detail="Servicio de transporte no encontrado")
    return transport_service


@router.put("/{transport_id}", response_model=TransportServiceResponse)
def update_transport_service(transport_id: int, transport_service: TransportServiceUpdate, db: Session = Depends(get_db)):
    db_transport_service = db.query(TransportService).filter(
        TransportService.TransportID == transport_id).first()
    if db_transport_service is None:
        raise HTTPException(
            status_code=404, detail="Servicio de transporte no encontrado")

    if transport_service.Capacity is not None:
        db_transport_service.Capacity = transport_service.Capacity
    if transport_service.DriverID is not None:
        db_transport_service.DriverID = transport_service.DriverID

    db.commit()
    db.refresh(db_transport_service)
    return db_transport_service


@router.delete("/{transport_id}")
def delete_transport_service(transport_id: int, db: Session = Depends(get_db)):
    db_transport_service = db.query(TransportService).filter(
        TransportService.TransportID == transport_id).first()
    if db_transport_service is None:
        raise HTTPException(
            status_code=404, detail="Servicio de transporte no encontrado")

    db.delete(db_transport_service)
    db.commit()
    return {"message": f"Servicio de transporte {transport_id} eliminado"}

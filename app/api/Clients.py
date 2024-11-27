from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Client
from app.schemas.ClientSchema import ClientCreate, ClientUpdate, ClientResponse
from app.services.ControlAccess import ControlAccess

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = Client(
        FirstName=client.FirstName,
        LastName=client.LastName,
        Email=client.Email,
        Password=client.Password,
        CountryID=client.CountryID,
        CityID=client.CityID,
        LanguageID=client.LanguageID,
        BirthDate=client.BirthDate
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@router.get("/", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.ClientID == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.ClientID == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db_client.FirstNama = client.FirstName or db_client.FirstName
    db_client.LastName = client.LastName or db_client.LastName
    db_client.Email = client.Email or db_client.Email
    db_client.Password = client.Password or db_client.Password

    db.commit()
    db.refresh(db_client)
    return db_client


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.ClientID == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db.delete(db_client)
    db.commit()
    return {"message": f"Cliente {client_id} eliminado"}


@router.put("/{client_id}/failedattempts")
def update_failed_attempts_endpoint(client_id: int, db: Session = Depends(get_db)):
    result = ControlAccess(client_id, db)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

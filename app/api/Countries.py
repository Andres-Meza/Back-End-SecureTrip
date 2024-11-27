from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Country
from app.schemas.CountrySchema import CountryCreate, CountryUpdate, CountryResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un nuevo país


@router.post("/", response_model=CountryResponse)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    existing_country = db.query(Country).filter(
        Country.NameCountry == country.NameCountry).first()
    if existing_country:
        raise HTTPException(
            status_code=400,
            detail="El país con este nombre ya existe.")

    # Si no existe, creamos el nuevo país
    db_country = Country(NameCountry=country.NameCountry)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


@router.get("/", response_model=list[CountryResponse])
def get_countries(db: Session = Depends(get_db)):
    return db.query(Country).all()


@router.get("/{country_id}", response_model=CountryResponse)
def get_country(country_id: int, db: Session = Depends(get_db)):
    country = db.query(Country).filter(Country.CountryID == country_id).first()
    if country is None:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return country


@router.put("/{country_id}", response_model=CountryResponse)
def update_country(country_id: int, country: CountryUpdate, db: Session = Depends(get_db)):
    db_country = db.query(Country).filter(
        Country.CountryID == country_id).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="País no encontrado")

    db_country.NameCountry = country.NameCountry

    db.commit()
    db.refresh(db_country)
    return db_country


@router.delete("/{country_id}")
def delete_country(country_id: int, db: Session = Depends(get_db)):
    db_country = db.query(Country).filter(
        Country.CountryID == country_id).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="País no encontrado")

    db.delete(db_country)
    db.commit()
    return {"message": f"País {country_id} eliminado"}

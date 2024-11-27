from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import City, Country
from app.schemas.CitySchema import CityCreate, CityUpdate, CityResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CityResponse)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    new_city = City(
        NameCity=city.NameCity,
        CountryID=city.CountryID
    )
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@router.get("/", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()


@router.get("/with-countries")
def get_cities_with_countries(db: Session = Depends(get_db)):
    cities_with_countries = db.query(City, Country).join(Country).all()
    return [
        {
            "cityId": city.CityID,
            "NameCity": city.NameCity,
            "NameCountry": country.NameCountry
        }
        for city, country in cities_with_countries
    ]


@router.get("/{city_id}", response_model=CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.CityID == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return city


@router.put("/{city_id}", response_model=CityResponse)
def update_city(city_id: int, city: CityUpdate, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.CityID == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")

    db_city.NameCity = city.NameCity
    db_city.CountryID = city.CountryID

    db.commit()
    db.refresh(db_city)
    return db_city


@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.CityID == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")

    db.delete(db_city)
    db.commit()
    return {"message": f"Ciudad {city_id} eliminada"}

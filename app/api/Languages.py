from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Language
from app.schemas.LanguageSchema import LanguageCreate, LanguageUpdate, LanguageResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=LanguageResponse)
def create_language(language: LanguageCreate, db: Session = Depends(get_db)):
    new_language = Language(NameLanguage=language.NameLanguage)
    db.add(new_language)
    db.commit()
    db.refresh(new_language)
    return new_language


@router.get("/", response_model=list[LanguageResponse])
def get_languages(db: Session = Depends(get_db)):
    return db.query(Language).all()


@router.get("/{language_id}", response_model=LanguageResponse)
def get_language(language_id: int, db: Session = Depends(get_db)):
    language = db.query(Language).filter(
        Language.LanguageID == language_id).first()
    if language is None:
        raise HTTPException(status_code=404, detail="Idioma no encontrado")
    return language


@router.put("/{language_id}", response_model=LanguageResponse)
def update_language(language_id: int, language: LanguageUpdate, db: Session = Depends(get_db)):
    db_language = db.query(Language).filter(
        Language.LanguageID == language_id).first()
    if db_language is None:
        raise HTTPException(status_code=404, detail="Idioma no encontrado")

    db_language.NameLanguage = language.NameLanguage

    db.commit()
    db.refresh(db_language)
    return db_language


@router.delete("/{language_id}")
def delete_language(language_id: int, db: Session = Depends(get_db)):
    db_language = db.query(Language).filter(
        Language.LanguageID == language_id).first()
    if db_language is None:
        raise HTTPException(status_code=404, detail="Idioma no encontrado")

    db.delete(db_language)
    db.commit()
    return {"message": f"Idioma {language_id} eliminado"}

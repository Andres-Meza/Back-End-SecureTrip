from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Collaborator
from app.schemas.CollaboratorSchema import CollaboratorCreate, CollaboratorUpdate, CollaboratorResponse
from app.utils.password import hashPassword

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_collaborator(collaborator: CollaboratorCreate, db: Session = Depends(get_db)):

    existingCollaborator = db.query(Collaborator).filter(
        Collaborator.Email == collaborator.Email).first()

    if existingCollaborator:
        raise HTTPException(
            status_code=400,
            detail="El email del cliente ya existe.")

    new_collaborator = Collaborator(
        FirstName=collaborator.FirstName,
        LastName=collaborator.LastName,
        Email=collaborator.Email,
        Password=hashPassword(collaborator.Password),
        TypeCollaborator=collaborator.TypeCollaborator,
        CountryID=collaborator.CountryID,
        CityID=collaborator.CityID,
        LanguageID=collaborator.LanguageID,
        Specialty=collaborator.Specialty,
        CompetencyLevel=collaborator.CompetencyLevel,
        LicenseType=collaborator.LicenseType,
        StatusCollaborator=collaborator.StatusCollaborator,
    )
    db.add(new_collaborator)
    db.commit()
    db.refresh(new_collaborator)
    return new_collaborator


@router.get("/", response_model=list[CollaboratorResponse])
def get_collaborators(db: Session = Depends(get_db)):
    return db.query(Collaborator).all()


@router.get("/{collaborator_id}", response_model=CollaboratorResponse)
def get_collaborator(collaborator_id: int, db: Session = Depends(get_db)):
    collaborator = db.query(Collaborator).filter(
        Collaborator.CollaboratorID == collaborator_id).first()
    if collaborator is None:
        raise HTTPException(
            status_code=404, detail="Colaborador no encontrado")
    return collaborator


@router.put("/{collaborator_id}", response_model=CollaboratorResponse)
def update_collaborator(collaborator_id: int, collaborator: CollaboratorUpdate, db: Session = Depends(get_db)):
    db_collaborator = db.query(Collaborator).filter(
        Collaborator.CollaboratorID == collaborator_id).first()
    if db_collaborator is None:
        raise HTTPException(
            status_code=404, detail="Colaborador no encontrado")

    if collaborator.FirstName:
        db_collaborator.FirstName = collaborator.FirstName
    if collaborator.LastName:
        db_collaborator.LastName = collaborator.LastName
    if collaborator.Email:
        db_collaborator.Email = collaborator.Email
    if collaborator.TypeCollaborator:
        db_collaborator.TypeCollaborator = collaborator.TypeCollaborator
    if collaborator.CountryID:
        db_collaborator.CountryID = collaborator.CountryID
    if collaborator.CityID:
        db_collaborator.CityID = collaborator.CityID
    if collaborator.LanguageID:
        db_collaborator.LanguageID = collaborator.LanguageID
    if collaborator.Specialty:
        db_collaborator.Specialty = collaborator.Specialty
    if collaborator.CompetencyLevel:
        db_collaborator.CompetencyLevel = collaborator.CompetencyLevel
    if collaborator.LicenseType:
        db_collaborator.LicenseType = collaborator.LicenseType
    if collaborator.StatusCollaborator:
        db_collaborator.StatusCollaborator = collaborator.StatusCollaborator

    db.commit()
    db.refresh(db_collaborator)
    return db_collaborator


@router.delete("/{collaborator_id}")
def delete_collaborator(collaborator_id: int, db: Session = Depends(get_db)):
    db_collaborator = db.query(Collaborator).filter(
        Collaborator.CollaboratorID == collaborator_id).first()
    if db_collaborator is None:
        raise HTTPException(
            status_code=404, detail="Colaborador no encontrado")

    db.delete(db_collaborator)
    db.commit()
    return {"message": f"Colaborador {collaborator_id} eliminado"}

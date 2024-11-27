from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Promotion
from app.schemas.PromotionSchema import PromotionCreate, PromotionUpdate, PromotionResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PromotionResponse)
def create_promotion(promotion: PromotionCreate, db: Session = Depends(get_db)):
    new_promotion = Promotion(
        Description=promotion.Description,
        Discount=promotion.Discount,
        StartDate=promotion.StartDate,
        EndDate=promotion.EndDate,
    )
    db.add(new_promotion)
    db.commit()
    db.refresh(new_promotion)
    return new_promotion


@router.get("/", response_model=list[PromotionResponse])
def get_promotions(db: Session = Depends(get_db)):
    return db.query(Promotion).all()


@router.get("/{promotion_id}", response_model=PromotionResponse)
def get_promotion(promotion_id: int, db: Session = Depends(get_db)):
    promotion = db.query(Promotion).filter(
        Promotion.PromotionID == promotion_id).first()
    if promotion is None:
        raise HTTPException(status_code=404, detail="Promoción no encontrada")
    return promotion


@router.put("/{promotion_id}", response_model=PromotionResponse)
def update_promotion(promotion_id: int, promotion: PromotionUpdate, db: Session = Depends(get_db)):
    db_promotion = db.query(Promotion).filter(
        Promotion.PromotionID == promotion_id).first()
    if db_promotion is None:
        raise HTTPException(status_code=404, detail="Promoción no encontrada")

    db_promotion.Description = promotion.Description
    db_promotion.Discount = promotion.Discount
    db_promotion.StartDate = promotion.StartDate
    db_promotion.EndDate = promotion.EndDate

    db.commit()
    db.refresh(db_promotion)
    return db_promotion


@router.delete("/{promotion_id}")
def delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    db_promotion = db.query(Promotion).filter(
        Promotion.PromotionID == promotion_id).first()
    if db_promotion is None:
        raise HTTPException(status_code=404, detail="Promoción no encontrada")

    db.delete(db_promotion)
    db.commit()
    return {"message": f"Promoción {promotion_id} eliminada"}

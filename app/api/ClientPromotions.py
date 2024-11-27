from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import ClientPromotion
from app.schemas.ClientPromotionSchema import ClientPromotionCreate, ClientPromotionResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ClientPromotionResponse)
def create_client_promotion(client_promotion: ClientPromotionCreate, db: Session = Depends(get_db)):
    new_client_promotion = ClientPromotion(
        ClientID=client_promotion.ClientID,
        PromotionID=client_promotion.PromotionID
    )
    db.add(new_client_promotion)
    db.commit()
    db.refresh(new_client_promotion)
    return new_client_promotion


@router.get("/", response_model=list[ClientPromotionResponse])
def get_client_promotions(db: Session = Depends(get_db)):
    return db.query(ClientPromotion).all()


@router.get("/{client_id}", response_model=list[ClientPromotionResponse])
def get_client_promotions_by_client(client_id: int, db: Session = Depends(get_db)):
    client_promotions = db.query(ClientPromotion).filter(
        ClientPromotion.ClientID == client_id).all()
    if not client_promotions:
        raise HTTPException(
            status_code=404, detail="No se encontraron promociones para este cliente.")
    return client_promotions

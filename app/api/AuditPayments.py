from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.AuditPayment import PaymentService
from app.models.Payment import Payment
from app.schemas.PaymentSchema import PaymentCreate

router = APIRouter()


@router.post("/")
def procesar_pago(payment: PaymentCreate, db: Session = Depends(get_db)):
    try:
        service = PaymentService()
        resultado = service.processPayment(db, payment.dict())
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

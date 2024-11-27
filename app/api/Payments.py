from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Payment
from app.schemas.PaymentSchema import PaymentCreate, PaymentUpdate, PaymentResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = Payment(
        ClientID=payment.ClientID,
        ServiceID=payment.ServiceID,
        Amount=payment.Amount,
        PaymentMethod=payment.PaymentMethod,
        IPAddress=payment.IPAddress,
        Reference=payment.Reference,
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.get("/", response_model=list[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.PaymentID == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return payment


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(
        Payment.PaymentID == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    db_payment.Status = payment.Status

    db.commit()
    db.refresh(db_payment)
    return db_payment


@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(
        Payment.PaymentID == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    db.delete(db_payment)
    db.commit()
    return {"message": f"Pago {payment_id} eliminado"}

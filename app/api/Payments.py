from sqlalchemy.sql import text
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app.models import Payment
from app.schemas.PaymentSchema import PaymentCreate, PaymentRequest, PaymentUpdate, PaymentResponse
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PaymentResponse)
async def registrar_pago(pago: PaymentRequest, db: Session = Depends(get_db)):
    try:
        stmt = text("""
            EXEC RegisterPayment 
                @ClientID = :ClientID, 
                @ServiceID = :ServiceID, 
                @Amount = :Amount, 
                @PaymentMethod = :PaymentMethod, 
                @IPAddress = :IPAddress, 
                @Reference = :Reference
        """)

        result = db.execute(stmt, {'ClientID': pago.ClientID, 'ServiceID': pago.ServiceID, 'Amount': pago.Amount,
                                   'PaymentMethod': pago.PaymentMethod, 'IPAddress': pago.IPAddress, 'Reference': pago.Reference})

        result_data = result.fetchone()

        if result_data:
            return {"mensaje": result_data[0]}
        else:
            raise HTTPException(
                status_code=400, detail="Error al registrar el pago")

    except Exception as e:
        print(f"Error al registrar el pago: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error en el servidor: {str(e)}")


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

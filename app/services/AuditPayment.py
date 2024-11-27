from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Service
from app.models.Payment import Payment
from fastapi import HTTPException


class PaymentService:
    def processPayment(self, db: Session, payment_data: dict):
        try:
            service = db.query(Service).filter(Service.ServiceID == payment_data['ServiceID']).first()
            if not service:
                raise HTTPException(status_code=404, detail="Service not found")
            
            payment_data['PaymentDate'] = datetime.now()
            newPayment = Payment(**payment_data)
            db.add(newPayment)
            db.commit()
            db.refresh(newPayment)

            if newPayment.Status == 'Pendiente Revision':
                return {
                    "mensaje": "Pago sospechoso requiere revisión",
                    "estado": "Pendiente Revision",
                    "monto": newPayment.Amount
                }

            return {"mensaje": "Pago procesado correctamente"}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

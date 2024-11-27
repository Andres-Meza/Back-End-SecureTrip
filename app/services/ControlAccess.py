from sqlalchemy import text
from app.database import engine
from sqlalchemy.orm import Session


def ControlAccess(db: Session, ClientID: int, Email: str, FailedAttempts: int):
    if FailedAttempts >= 3:
        consulta_bloqueo = text("""
            UPDATE Client 
            SET ClientStatus = 'Bloqueado' 
            WHERE ClientID = :ClientID
        """)

        db.execute(consulta_bloqueo, {
            'ClientID': ClientID
        })
        db.commit()

        print(f'ALERTA: Cuenta de {Email} bloqueada tras {
              FailedAttempts} intentos fallidos')
        return True
    return False

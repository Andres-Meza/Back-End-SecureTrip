from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.password import verifyPassword
from app.services.ControlAccess import ControlAccess

router = APIRouter()


class LoginRequest(BaseModel):
    Email: str
    Password: str


@router.post("/")
def iniciar_sesion(
    loginData: LoginRequest,
    db: Session = Depends(get_db)
):
    consulta_login = text("""
        SELECT ClientID, Password, FailedAttempts, ClientStatus
        FROM Client
        WHERE Email = :Email
    """)
    resultado = db.execute(
        consulta_login, {'Email': loginData.Email}).fetchone()

    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    ClientID, Password_Hash, FailedAttempts, ClientStatus = resultado

    if ClientStatus == 'Bloqueado':
        raise HTTPException(
            status_code=403, detail="Cuenta bloqueada por demasiados intentos fallidos")

    if not verifyPassword(loginData.Password, Password_Hash):
        incrementar_intentos(db, loginData.Email)

        ControlAccess(
            db,
            ClientID,
            loginData.Email,
            FailedAttempts + 1
        )

        if FailedAttempts + 1 >= 3:
            bloquear_cuenta(db, loginData.Email)
            raise HTTPException(
                status_code=403, detail="Cuenta bloqueada por demasiados intentos fallidos")

        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    resetear_intentos(db, loginData.Email)

    return {"mensaje": "Inicio de sesión exitoso", "ClientID": ClientID}


def incrementar_intentos(db: Session, email: str):
    consulta_incremento = text("""
        UPDATE Client 
        SET FailedAttempts = FailedAttempts + 1 
        WHERE Email = :Email
    """)
    db.execute(consulta_incremento, {'Email': email})
    db.commit()


def bloquear_cuenta(db: Session, email: str):
    consulta_bloqueo = text("""
        UPDATE Client 
        SET ClientStatus = 'Bloqueado' 
        WHERE Email = :Email
    """)
    db.execute(consulta_bloqueo, {'Email': email})
    db.commit()


def resetear_intentos(db: Session, email: str):
    consulta_reset = text("""
        UPDATE Client
        SET FailedAttempts = 0 
        WHERE Email = :Email
    """)
    db.execute(consulta_reset, {'Email': email})
    db.commit()

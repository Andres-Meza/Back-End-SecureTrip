from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ControlAccess import ControlAccess

router = APIRouter()


class LoginRequest(BaseModel):
    Email: str
    Password: str


@router.post("/")
def iniciar_sesion(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    consulta_login = text("""
				SELECT ClientID, Password, FailedAttempts, ClientStatus
				FROM Client
				WHERE Email = :Email
		""")

    resultado = db.execute(
        consulta_login, {'Email': login_data.Email}).fetchone()

    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    ClientID, Password_Save, FailedAttempts, ClientStatus = resultado

    if ClientStatus == 'Bloqueado':
        raise HTTPException(status_code=403, detail="Cuenta bloqueada")

    if login_data.Password != Password_Save:
        consulta_incremento = text("""
						UPDATE Client 
						SET FailedAttempts = FailedAttempts + 1 
						WHERE Email = :Email
				""")
        db.execute(consulta_incremento, {'Email': login_data.Email})
        db.commit()

        ControlAccess(
            db,
            ClientID,
            login_data.Email,
            FailedAttempts + 1
        )

        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    consulta_reset = text("""
				UPDATE Client
				SET FailedAttempts = 0 
				WHERE Email = :Email
		""")
    db.execute(consulta_reset, {'Email': login_data.Email})
    db.commit()

    return {"mensaje": "Inicio de sesión exitoso"}

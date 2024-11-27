from sqlalchemy import text
from app.database import engine
from sqlalchemy.orm import Session


def ControlAccess(client_id: int, db: Session):
    try:
        db.execute(text("""
						UPDATE Clientes
						SET IntentosFallidos = IntentosFallidos + 1
						WHERE ClienteID = :client_id
				"""), {"client_id": client_id})
        db.commit()
        return {"message": "Intentos fallidos actualizados, trigger ejecutado si es necesario."}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al actualizar intentos fallidos: {e}"}

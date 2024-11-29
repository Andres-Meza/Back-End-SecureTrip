from database import Base, engine
from models import *


def create_tables():
    try:
        print("Creando las tablas en la base de datos...")
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas con éxito.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")


if __name__ == "__main__":
    create_tables()

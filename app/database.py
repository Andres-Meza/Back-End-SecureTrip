from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuración de la conexión a la base de datos
SERVER = "MSI\\SQLEXPRESS"
DATABASE = "SecureTripF"
DATABASE_URL = f"mssql+pyodbc://{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener la sesión de la base de datos


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para probar la conexión


def test_connection():
    try:
        with engine.connect() as connection:
            # Ejecutar una consulta de prueba
            result = connection.execute(text("SELECT 1"))
            print("Conexión exitosa a la base de datos. Resultado:", result.scalar())
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")


# Ejecutar la prueba de conexión si este archivo se ejecuta directamente
if __name__ == "__main__":
    test_connection()

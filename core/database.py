from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

class Base(DeclarativeBase):
    pass


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/cesfam_db"

#crea el motor de la conexion a la base de datos asincronico
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Para ver las consultas SQL
    future=True # Para usar SQLAlchemy 2.0
)

#es como una fabrica de sesiones
#expirar = que cuando se cierre la sesion, se borren los datos
#en desarrollo es false, en produccion es true
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession, #crea sessiones asincronicas
    expire_on_commit=False #no expirar la sesion al cerrarla
)

#funcion que genera sesiones y se la da a los endpoints
async def get_db():
    async with AsyncSessionLocal() as session: #abre la sesion
        yield session #entrega la sesion a quien la pida y despues la cierra
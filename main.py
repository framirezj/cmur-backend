from fastapi import FastAPI
from features.enlaces.router import router as enlaces_router
from features.usuarios.router import router as usuarios_router
from features.indicadores.router import router as indicadores_router
from features.anexos.router import router as anexos_router
import features.usuarios.models  # noqa: F401 — registra tablas en Base.metadata
import features.anexos.models  # noqa: F401 — registra tablas en Base.metadata
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
from core.database import engine, Base
from fastapi.staticfiles import StaticFiles
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Verificando conexión a la base de datos...")

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Base de datos conectada correctamente.")

        print("🔄 Creando tablas en la base de datos...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas/verificadas correctamente.")
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        raise

    yield

    await engine.dispose()



app = FastAPI(title="Portal Enlaces CESFAM",
            description="",
            version="0.0.1",
            lifespan=lifespan
            )

#sirve los logos
app.mount(
    "/logos",
    StaticFiles(directory=settings.UPLOAD_DIR),
    name="logos",
)

# Habilitar CORS para que React se conecte sin problemas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambiar por el URL de React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#ROUTERS       
app.include_router(enlaces_router)
app.include_router(usuarios_router)
app.include_router(indicadores_router)
app.include_router(anexos_router)

#STATUS
@app.get("/health",tags=["Health"])
async def health():
    return {"status":"ok",
            "info":"Portal Enlaces CESFAM"
    }




#uv run fastapi dev main.py
from fastapi import FastAPI
from features.enlaces.router import router as enlaces_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
from core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Verificando conexión a la base de datos...")

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Base de datos conectada correctamente.")
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

#STATUS
@app.get("/health",tags=["Health"])
async def health():
    return {"status":"ok",
            "info":"Portal Enlaces CESFAM"
    }




#uv run fastapi dev main.py
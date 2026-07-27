from fastapi import FastAPI
from features.enlaces.router import router as enlaces_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Portal Enlaces CESFAM",
            description="",
            version="0.0.1")



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
@app.get("/status",tags=["Status"])
def status():
    return {"status":"ok",
            "info":"Portal Enlaces CESFAM"
    }




#uv run fastapi dev main.py
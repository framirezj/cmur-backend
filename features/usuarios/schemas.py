from pydantic import BaseModel, EmailStr
from datetime import datetime
from features.enlaces.schemas import EnlaceResponse


# ── Auth ─────────────────────────────────────────────────────────────────────

class GoogleLoginRequest(BaseModel):
    """Cuerpo del POST /auth/google — el cliente envía el id_token de Google."""
    id_token: str


class TokenResponse(BaseModel):
    """Respuesta del login: JWT propio + datos básicos del usuario."""
    access_token: str
    token_type: str = "bearer"
    usuario: "UsuarioResponse"


# ── Usuario ───────────────────────────────────────────────────────────────────

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    foto_url: str | None
    created_at: datetime

    class Config:
        from_attributes = True


# ── Favoritos ─────────────────────────────────────────────────────────────────

class FavoritoResponse(BaseModel):
    """Enlace favorito del usuario, incluye fecha en que fue agregado."""
    enlace: EnlaceResponse
    created_at: datetime

    class Config:
        from_attributes = True


# Resolución de referencia forward
TokenResponse.model_rebuild()

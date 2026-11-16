from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re
from features.enlaces.schemas import EnlaceResponse


def normalizar_rut(v: str) -> str:
    """Limpia puntos y espacios, y pasa el dígito verificador a mayúscula."""
    limpio = re.sub(r"[.\s]", "", v).strip().upper()
    if not limpio:
        raise ValueError("El RUT no puede estar vacío")
    return limpio


# ── Auth ─────────────────────────────────────────────────────────────────────

class RegistroRequest(BaseModel):
    """Cuerpo del POST /auth/register — Registro de nuevo funcionario."""
    rut: str = Field(..., description="RUT del funcionario (ej: 12.345.678-9 o 12345678-9)")
    nombre: str = Field(..., min_length=2, max_length=200, description="Nombre completo")
    pin: str = Field(..., pattern=r"^\d{4}$", description="PIN de acceso de exactamente 4 dígitos numéricos")
    email: EmailStr | None = Field(default=None, description="Correo electrónico (opcional)")

    @field_validator("rut")
    @classmethod
    def validar_rut(cls, v: str) -> str:
        return normalizar_rut(v)


class LoginRequest(BaseModel):
    """Cuerpo del POST /auth/login — Inicio de sesión con RUT y PIN."""
    rut: str = Field(..., description="RUT del funcionario")
    pin: str = Field(..., pattern=r"^\d{4}$", description="PIN de acceso de 4 dígitos")

    @field_validator("rut")
    @classmethod
    def validar_rut(cls, v: str) -> str:
        return normalizar_rut(v)


class TokenResponse(BaseModel):
    """Respuesta del login/registro: JWT propio + datos básicos del usuario."""
    access_token: str
    token_type: str = "bearer"
    usuario: "UsuarioResponse"


# ── Usuario ───────────────────────────────────────────────────────────────────

class UsuarioResponse(BaseModel):
    id: int
    rut: str
    nombre: str
    rol: str
    email: str | None
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

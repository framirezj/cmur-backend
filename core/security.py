from datetime import datetime, timedelta, timezone
import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings

# Esquema de seguridad: espera el header "Authorization: Bearer <token>"
bearer_scheme = HTTPBearer()


# ── Hash de PIN ───────────────────────────────────────────────────────────────

def hash_pin(pin: str) -> str:
    """Genera el hash seguro de un PIN de 4 dígitos usando bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pin.encode("utf-8"), salt).decode("utf-8")


def verify_pin(plain_pin: str, hashed_pin: str) -> bool:
    """Verifica si un PIN en texto plano coincide con su hash."""
    try:
        return bcrypt.checkpw(plain_pin.encode("utf-8"), hashed_pin.encode("utf-8"))
    except Exception:
        return False


# ── JWT ───────────────────────────────────────────────────────────────────────

def create_access_token(data: dict) -> str:
    """
    Genera un JWT propio firmado con JWT_SECRET_KEY.
    Incluye 'sub' (usuario.id), 'rol' y la expiración en JWT_EXPIRE_MINUTES.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decodifica y valida el JWT propio.
    Lanza HTTPException 401 si es inválido o expirado.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ── Dependencias de autenticación y autorización ──────────────────────────────

def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Extrae y decodifica el payload del JWT de la cabecera Authorization."""
    return decode_access_token(credentials.credentials)


def get_current_user_id(
    payload: dict = Depends(get_current_user_payload),
) -> int:
    """
    Dependencia FastAPI: extrae el usuario_id del JWT.
    Uso: usuario_id: int = Depends(get_current_user_id)
    """
    usuario_id: str | None = payload.get("sub")
    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sin identidad de usuario",
        )
    return int(usuario_id)


def require_admin(
    payload: dict = Depends(get_current_user_payload),
) -> int:
    """
    Dependencia FastAPI: verifica que el usuario autenticado posea rol 'admin'.
    Si el rol es 'usuario' u otro, lanza 403 Forbidden.
    Retorna el usuario_id del administrador.
    """
    usuario_id = get_current_user_id(payload)
    rol: str = payload.get("rol", "usuario")
    if rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permiso denegado: se requiere rol de administrador para realizar esta acción.",
        )
    return usuario_id

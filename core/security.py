from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings

# Esquema de seguridad: espera el header "Authorization: Bearer <token>"
bearer_scheme = HTTPBearer()


def verify_google_token(token: str) -> dict:
    """
    Verifica el id_token emitido por Google Identity Services.
    Retorna el payload con: sub, email, name, picture, etc.
    Lanza ValueError si el token es inválido o expirado.
    """
    try:
        payload = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
        return payload
    except Exception as e:
        raise ValueError(f"Token de Google inválido: {e}")


def create_access_token(data: dict) -> str:
    """
    Genera un JWT propio firmado con JWT_SECRET_KEY.
    Incluye la expiración definida en JWT_EXPIRE_MINUTES.
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


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> int:
    """
    Dependencia FastAPI: extrae el usuario_id del JWT del header Authorization.
    Uso: usuario_id: int = Depends(get_current_user_id)
    """
    payload = decode_access_token(credentials.credentials)
    usuario_id: int | None = payload.get("sub")
    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sin identidad de usuario",
        )
    return int(usuario_id)

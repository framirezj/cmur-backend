from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.security import get_current_user_id
from features.usuarios.service import UsuarioService
from features.usuarios.repository import UsuarioRepository
from features.usuarios.schemas import (
    GoogleLoginRequest,
    TokenResponse,
    UsuarioResponse,
    FavoritoResponse,
)


router = APIRouter(tags=["Usuarios"])


# ── Dependencia de servicio ───────────────────────────────────────────────────

def get_service(db: AsyncSession = Depends(get_db)) -> UsuarioService:
    return UsuarioService(repo=UsuarioRepository(db=db))


# ── Auth ──────────────────────────────────────────────────────────────────────

@router.post(
    "/auth/google",
    response_model=TokenResponse,
    summary="Login con Google",
    description="Recibe el **id_token** de Google Identity Services, valida la identidad, "
                "crea el usuario si es la primera vez, y retorna el JWT de la aplicación.",
)
async def login_google(
    body: GoogleLoginRequest,
    service: UsuarioService = Depends(get_service),
):
    return await service.login_con_google(body.id_token)


# ── Perfil ────────────────────────────────────────────────────────────────────

@router.get(
    "/usuarios/me",
    response_model=UsuarioResponse,
    summary="Perfil del usuario autenticado",
)
async def obtener_perfil(
    usuario_id: int = Depends(get_current_user_id),
    service: UsuarioService = Depends(get_service),
):
    return await service.obtener_usuario(usuario_id)


# ── Favoritos ─────────────────────────────────────────────────────────────────

@router.get(
    "/usuarios/me/favoritos",
    response_model=list[FavoritoResponse],
    summary="Listar enlaces favoritos del usuario",
)
async def listar_favoritos(
    usuario_id: int = Depends(get_current_user_id),
    service: UsuarioService = Depends(get_service),
):
    return await service.listar_favoritos(usuario_id)


@router.post(
    "/usuarios/me/favoritos/{enlace_id}",
    response_model=FavoritoResponse,
    status_code=201,
    summary="Agregar un enlace a favoritos",
)
async def agregar_favorito(
    enlace_id: int,
    usuario_id: int = Depends(get_current_user_id),
    service: UsuarioService = Depends(get_service),
):
    return await service.agregar_favorito(usuario_id, enlace_id)


@router.delete(
    "/usuarios/me/favoritos/{enlace_id}",
    status_code=204,
    summary="Eliminar un enlace de favoritos",
)
async def eliminar_favorito(
    enlace_id: int,
    usuario_id: int = Depends(get_current_user_id),
    service: UsuarioService = Depends(get_service),
):
    await service.eliminar_favorito(usuario_id, enlace_id)

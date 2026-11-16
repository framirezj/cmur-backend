from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.security import get_current_user_id
from features.usuarios.service import UsuarioService
from features.usuarios.repository import UsuarioRepository
from features.usuarios.schemas import (
    RegistroRequest,
    LoginRequest,
    TokenResponse,
    UsuarioResponse,
    FavoritoResponse,
)


router = APIRouter(tags=["Usuarios & Autenticación"])


# ── Dependencia de servicio ───────────────────────────────────────────────────

def get_service(db: AsyncSession = Depends(get_db)) -> UsuarioService:
    return UsuarioService(repo=UsuarioRepository(db=db))


# ── Auth ──────────────────────────────────────────────────────────────────────

@router.post(
    "/auth/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registro de funcionario",
    description="Registra un funcionario mediante su RUT y un PIN numérico de 4 dígitos. "
                "Se le asigna automáticamente el rol 'usuario'.",
)
async def registrar_usuario(
    body: RegistroRequest,
    service: UsuarioService = Depends(get_service),
):
    return await service.registrar(body)


@router.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Iniciar sesión con RUT y PIN",
    description="Autentica a un funcionario validando su RUT y PIN de 4 dígitos. Retorna el JWT de acceso.",
)
async def login_usuario(
    body: LoginRequest,
    service: UsuarioService = Depends(get_service),
):
    return await service.login(body)


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
    status_code=status.HTTP_201_CREATED,
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
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un enlace de favoritos",
)
async def eliminar_favorito(
    enlace_id: int,
    usuario_id: int = Depends(get_current_user_id),
    service: UsuarioService = Depends(get_service),
):
    await service.eliminar_favorito(usuario_id, enlace_id)

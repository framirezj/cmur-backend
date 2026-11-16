from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.security import get_current_user_id, require_admin
from features.anexos.service import AnexoService
from features.anexos.repository import AnexoRepository
from features.anexos.schemas import AnexoResponse, AnexoCreate, AnexoUpdate, PaginatedAnexoResponse
from typing import Optional

router = APIRouter(prefix="/anexos", tags=["Anexos"])


def get_service(db: AsyncSession = Depends(get_db)) -> AnexoService:
    return AnexoService(repo=AnexoRepository(db=db))


@router.get(
    "/",
    response_model=PaginatedAnexoResponse,
    summary="Listar todos los anexos telefónicos",
    description="Obtiene el listado de anexos con posibilidad de filtrar por búsqueda de texto o unidad de servicio.",
)
async def listar_anexos(
    search: Optional[str] = Query(None, description="Búsqueda por texto (anexo, ubicación, unidad, funcionarios)"),
    unidad_servicio: Optional[str] = Query(None, alias="unidadServicio", description="Filtro por unidad de servicio"),
    page: int = Query(1, ge=1, description="Número de página (1-based)"),
    size: int = Query(20, ge=1, le=100, description="Cantidad de elementos por página"),
    service: AnexoService = Depends(get_service),
):
    items, total = await service.listar_anexos(
        search=search,
        unidad_servicio=unidad_servicio,
        page=page,
        size=size,
    )
    pages = (total + size - 1) // size if total > 0 else 0
    return PaginatedAnexoResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get(
    "/{anexo_id}",
    response_model=AnexoResponse,
    summary="Obtener un anexo por ID",
)
async def obtener_anexo(
    anexo_id: int,
    service: AnexoService = Depends(get_service),
):
    return await service.obtener_anexo(anexo_id)


@router.post(
    "/",
    response_model=AnexoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo anexo",
    description="Requiere rol de administrador (Bearer Token). Registra el usuario creador.",
)
async def crear_anexo(
    body: AnexoCreate,
    usuario_id: int = Depends(require_admin),
    service: AnexoService = Depends(get_service),
):
    return await service.crear_anexo(body, usuario_id=usuario_id)


@router.put(
    "/{anexo_id}",
    response_model=AnexoResponse,
    summary="Actualizar un anexo",
    description="Requiere rol de administrador (Bearer Token). Registra el usuario que realizó la actualización.",
)
async def actualizar_anexo(
    anexo_id: int,
    body: AnexoUpdate,
    usuario_id: int = Depends(require_admin),
    service: AnexoService = Depends(get_service),
):
    return await service.actualizar_anexo(anexo_id, body, usuario_id=usuario_id)


@router.delete(
    "/{anexo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un anexo",
    description="Requiere rol de administrador (Bearer Token).",
)
async def eliminar_anexo(
    anexo_id: int,
    usuario_id: int = Depends(require_admin),
    service: AnexoService = Depends(get_service),
):
    await service.eliminar_anexo(anexo_id, usuario_id=usuario_id)

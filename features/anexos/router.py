from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from features.anexos.service import AnexoService
from features.anexos.repository import AnexoRepository
from features.anexos.schemas import AnexoResponse, AnexoCreate, AnexoUpdate
from typing import Optional

router = APIRouter(prefix="/anexos", tags=["Anexos"])


def get_service(db: AsyncSession = Depends(get_db)) -> AnexoService:
    return AnexoService(repo=AnexoRepository(db=db))


@router.get(
    "/",
    response_model=list[AnexoResponse],
    summary="Listar todos los anexos telefónicos",
    description="Obtiene el listado de anexos con posibilidad de filtrar por búsqueda de texto o unidad de servicio.",
)
async def listar_anexos(
    search: Optional[str] = Query(None, description="Búsqueda por texto (anexo, ubicación, unidad, funcionarios)"),
    unidad_servicio: Optional[str] = Query(None, alias="unidadServicio", description="Filtro por unidad de servicio"),
    service: AnexoService = Depends(get_service),
):
    return await service.listar_anexos(search=search, unidad_servicio=unidad_servicio)


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
)
async def crear_anexo(
    body: AnexoCreate,
    service: AnexoService = Depends(get_service),
):
    return await service.crear_anexo(body)


@router.put(
    "/{anexo_id}",
    response_model=AnexoResponse,
    summary="Actualizar un anexo",
)
async def actualizar_anexo(
    anexo_id: int,
    body: AnexoUpdate,
    service: AnexoService = Depends(get_service),
):
    return await service.actualizar_anexo(anexo_id, body)


@router.delete(
    "/{anexo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un anexo",
)
async def eliminar_anexo(
    anexo_id: int,
    service: AnexoService = Depends(get_service),
):
    await service.eliminar_anexo(anexo_id)

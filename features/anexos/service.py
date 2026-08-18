from typing import Sequence
from fastapi import HTTPException, status
from features.anexos.repository import AnexoRepository
from features.anexos.models import Anexo
from features.anexos.schemas import AnexoCreate, AnexoUpdate


class AnexoService:
    def __init__(self, repo: AnexoRepository):
        self.repo = repo

    async def listar_anexos(
        self,
        search: str | None = None,
        unidad_servicio: str | None = None,
    ) -> Sequence[Anexo]:
        return await self.repo.get_all(search=search, unidad_servicio=unidad_servicio)

    async def obtener_anexo(self, anexo_id: int) -> Anexo:
        anexo = await self.repo.get_by_id(anexo_id)
        if not anexo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anexo no encontrado",
            )
        return anexo

    async def crear_anexo(self, data: AnexoCreate, usuario_id: int) -> Anexo:
        return await self.repo.create(data, usuario_id=usuario_id)

    async def actualizar_anexo(self, anexo_id: int, data: AnexoUpdate, usuario_id: int) -> Anexo:
        anexo = await self.repo.update(anexo_id, data, usuario_id=usuario_id)
        if not anexo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anexo no encontrado",
            )
        return anexo

    async def eliminar_anexo(self, anexo_id: int, usuario_id: int) -> None:
        deleted = await self.repo.delete(anexo_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anexo no encontrado",
            )

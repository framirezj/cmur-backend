from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import Sequence
from features.anexos.models import Anexo
from features.anexos.schemas import AnexoCreate, AnexoUpdate

INITIAL_ANEXOS = [
    {
        "id": 1,
        "anexo": "101",
        "ubicacion": "Segundo Piso, Ala Norte",
        "unidad_servicio": "SECTOR ROJO",
        "funcionarios": "Sra. Jefa (Directora)",
    },
    {
        "id": 2,
        "anexo": "102",
        "ubicacion": "Primer Piso, Pasillo Central",
        "unidad_servicio": "SECTOR VERDE",
        "funcionarios": "E.U. Pérez y E.U. Gómez",
    },
    {
        "id": 3,
        "anexo": "201",
        "ubicacion": "Módulo 3",
        "unidad_servicio": "SECTOR AZUL",
        "funcionarios": "Dr. Rojas / Enfermera María",
    },
    {
        "id": 4,
        "anexo": "301",
        "ubicacion": "Edificio Anexo",
        "unidad_servicio": "SECTOR AMARILLO",
        "funcionarios": "Téc. Dentista López",
    },
    {
        "id": 5,
        "anexo": "302",
        "ubicacion": "Sala multiuso",
        "unidad_servicio": "SECTOR TRANSVERSAL",
        "funcionarios": "Administrativos",
    },
]


class AnexoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def seed_if_empty(self) -> None:
        query = select(Anexo)
        result = await self.db.execute(query)
        existing = result.scalars().first()
        if not existing:
            for data in INITIAL_ANEXOS:
                anexo_obj = Anexo(
                    id=data["id"],
                    anexo=data["anexo"],
                    ubicacion=data["ubicacion"],
                    unidad_servicio=data["unidad_servicio"],
                    funcionarios=data["funcionarios"],
                )
                self.db.add(anexo_obj)
            await self.db.commit()

    async def get_all(
        self,
        search: str | None = None,
        unidad_servicio: str | None = None,
    ) -> Sequence[Anexo]:
        await self.seed_if_empty()
        query = select(Anexo).order_by(Anexo.id.asc())

        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(
                    Anexo.anexo.ilike(pattern),
                    Anexo.ubicacion.ilike(pattern),
                    Anexo.unidad_servicio.ilike(pattern),
                    Anexo.funcionarios.ilike(pattern),
                )
            )

        if unidad_servicio:
            query = query.where(Anexo.unidad_servicio == unidad_servicio)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, anexo_id: int) -> Anexo | None:
        await self.seed_if_empty()
        query = select(Anexo).where(Anexo.id == anexo_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: AnexoCreate) -> Anexo:
        anexo_obj = Anexo(
            anexo=data.anexo,
            ubicacion=data.ubicacion,
            unidad_servicio=data.unidadServicio,
            funcionarios=data.funcionarios,
        )
        self.db.add(anexo_obj)
        await self.db.commit()
        await self.db.refresh(anexo_obj)
        return anexo_obj

    async def update(self, anexo_id: int, data: AnexoUpdate) -> Anexo | None:
        anexo_obj = await self.get_by_id(anexo_id)
        if not anexo_obj:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "unidadServicio" in update_data:
            update_data["unidad_servicio"] = update_data.pop("unidadServicio")

        for key, value in update_data.items():
            setattr(anexo_obj, key, value)

        await self.db.commit()
        await self.db.refresh(anexo_obj)
        return anexo_obj

    async def delete(self, anexo_id: int) -> bool:
        anexo_obj = await self.get_by_id(anexo_id)
        if not anexo_obj:
            return False
        await self.db.delete(anexo_obj)
        await self.db.commit()
        return True

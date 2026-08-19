from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import Sequence
from features.anexos.models import Anexo
from features.anexos.schemas import AnexoCreate, AnexoUpdate
from sqlalchemy import text

INITIAL_ANEXOS = [
    {
        "id": 1000,
        "anexo": "101",
        "ubicacion": "Segundo Piso, Ala Norte",
        "unidad_servicio": "SECTOR ROJO",
        "funcionarios": "Sra. Jefa (Directora)",
    },
    {
        "id": 1001,
        "anexo": "102",
        "ubicacion": "Primer Piso, Pasillo Central",
        "unidad_servicio": "SECTOR VERDE",
        "funcionarios": "E.U. Pérez y E.U. Gómez",
    },
    {
        "id": 1002,
        "anexo": "201",
        "ubicacion": "Módulo 3",
        "unidad_servicio": "SECTOR AZUL",
        "funcionarios": "Dr. Rojas / Enfermera María",
    },
    {
        "id": 1003,
        "anexo": "301",
        "ubicacion": "Edificio Anexo",
        "unidad_servicio": "SECTOR AMARILLO",
        "funcionarios": "Téc. Dentista López",
    },
    {
        "id": 1004,
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
            # Ejecutar el INSERT directamente
            insert_query = text("""
                INSERT INTO anexos (
                    anexo,
                    ubicacion,
                    unidad_servicio,
                    funcionarios,
                    creado_por_id,
                    actualizado_por_id
                )
                SELECT 
                    generate_series(500, 599) AS anexo,
                    'Sin asignar',
                    'Sin asignar',
                    'Sin asignar',
                    NULL,
                    NULL
            """)
            
            await self.db.execute(insert_query)
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

    async def create(self, data: AnexoCreate, usuario_id: int | None = None) -> Anexo:
        anexo_obj = Anexo(
            anexo=data.anexo,
            ubicacion=data.ubicacion,
            unidad_servicio=data.unidadServicio,
            funcionarios=data.funcionarios,
            creado_por_id=usuario_id,
            actualizado_por_id=usuario_id,
        )
        self.db.add(anexo_obj)
        await self.db.commit()
        await self.db.refresh(anexo_obj)
        return anexo_obj

    async def update(self, anexo_id: int, data: AnexoUpdate, usuario_id: int | None = None) -> Anexo | None:
        anexo_obj = await self.get_by_id(anexo_id)
        if not anexo_obj:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "unidadServicio" in update_data:
            update_data["unidad_servicio"] = update_data.pop("unidadServicio")

        for key, value in update_data.items():
            setattr(anexo_obj, key, value)

        if usuario_id is not None:
            anexo_obj.actualizado_por_id = usuario_id

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

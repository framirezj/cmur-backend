from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete
from features.usuarios.models import Usuario, Favorito
from features.enlaces.models import Enlace


class UsuarioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Usuarios ──────────────────────────────────────────────────────────────

    async def get_by_google_sub(self, google_sub: str) -> Usuario | None:
        """Busca un usuario por su ID único de Google (sub)."""
        result = await self.db.execute(
            select(Usuario).where(Usuario.google_sub == google_sub)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, usuario_id: int) -> Usuario | None:
        """Busca un usuario por su ID interno."""
        result = await self.db.execute(
            select(Usuario).where(Usuario.id == usuario_id)
        )
        return result.scalar_one_or_none()

    async def crear(self, usuario: Usuario) -> Usuario:
        """Persiste un nuevo usuario en la base de datos."""
        self.db.add(usuario)
        await self.db.commit()
        await self.db.refresh(usuario)
        return usuario

    # ── Favoritos ─────────────────────────────────────────────────────────────

    async def get_favoritos(self, usuario_id: int) -> list[Favorito]:
        """Retorna todos los favoritos de un usuario, con el enlace cargado."""
        result = await self.db.execute(
            select(Favorito)
            .where(Favorito.usuario_id == usuario_id)
            .options(selectinload(Favorito.enlace))
            .order_by(Favorito.created_at.desc())
        )
        return list(result.scalars().all())

    async def favorito_existe(self, usuario_id: int, enlace_id: int) -> bool:
        """Verifica si ya existe la relación favorito."""
        result = await self.db.execute(
            select(Favorito).where(
                Favorito.usuario_id == usuario_id,
                Favorito.enlace_id == enlace_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def agregar_favorito(self, usuario_id: int, enlace_id: int) -> Favorito:
        """Inserta un nuevo favorito y lo retorna con el enlace cargado."""
        favorito = Favorito(usuario_id=usuario_id, enlace_id=enlace_id)
        self.db.add(favorito)
        await self.db.commit()
        # Cargar el enlace relacionado para retornarlo completo
        result = await self.db.execute(
            select(Favorito)
            .where(Favorito.usuario_id == usuario_id, Favorito.enlace_id == enlace_id)
            .options(selectinload(Favorito.enlace))
        )
        return result.scalar_one()

    async def eliminar_favorito(self, usuario_id: int, enlace_id: int) -> bool:
        """Elimina un favorito. Retorna True si existía, False si no."""
        result = await self.db.execute(
            delete(Favorito).where(
                Favorito.usuario_id == usuario_id,
                Favorito.enlace_id == enlace_id,
            )
        )
        await self.db.commit()
        return result.rowcount > 0

    async def get_enlace_by_id(self, enlace_id: int) -> Enlace | None:
        """Verifica que el enlace existe antes de agregar como favorito."""
        result = await self.db.execute(
            select(Enlace).where(Enlace.id == enlace_id)
        )
        return result.scalar_one_or_none()

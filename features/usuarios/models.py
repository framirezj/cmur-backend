from datetime import datetime, timezone
from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, UniqueConstraint


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    google_sub: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    foto_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relación: un usuario tiene muchos favoritos
    favoritos: Mapped[list["Favorito"]] = relationship("Favorito", back_populates="usuario", cascade="all, delete-orphan")


class Favorito(Base):
    __tablename__ = "favoritos"

    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    enlace_id: Mapped[int] = mapped_column(Integer, ForeignKey("enlaces.id", ondelete="CASCADE"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relaciones
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="favoritos")
    enlace: Mapped["Enlace"] = relationship("Enlace")


# Importación diferida para evitar circular imports
from features.enlaces.models import Enlace  # noqa: E402, F401

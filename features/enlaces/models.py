import enum
from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum

class CategoriaEnlace(str, enum.Enum):
    SIDRA = "SIDRA"
    OTROS = "OTROS"

class Enlace(Base):
    __tablename__ = "enlaces"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    categoria: Mapped[CategoriaEnlace] = mapped_column(Enum(CategoriaEnlace), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    imagen_path: Mapped[str] = mapped_column(String(500), nullable=False)
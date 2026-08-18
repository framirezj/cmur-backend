from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Anexo(Base):
    __tablename__ = "anexos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    anexo: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    ubicacion: Mapped[str] = mapped_column(String(255), nullable=False)
    unidad_servicio: Mapped[str] = mapped_column(String(255), nullable=False)
    funcionarios: Mapped[str] = mapped_column(String(255), nullable=False)

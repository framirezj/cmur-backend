from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

class AnexoBase(BaseModel):
    anexo: str
    ubicacion: str
    unidadServicio: str = Field(..., validation_alias="unidad_servicio", serialization_alias="unidadServicio")
    funcionarios: str

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class AnexoCreate(AnexoBase):
    pass

class AnexoUpdate(BaseModel):
    anexo: Optional[str] = None
    ubicacion: Optional[str] = None
    unidadServicio: Optional[str] = Field(None, validation_alias="unidad_servicio", serialization_alias="unidadServicio")
    funcionarios: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class AnexoResponse(AnexoBase):
    id: str
    creado_por_id: Optional[int] = Field(None, validation_alias="creado_por_id", serialization_alias="creadoPorId")
    actualizado_por_id: Optional[int] = Field(None, validation_alias="actualizado_por_id", serialization_alias="actualizadoPorId")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v):
        if v is not None:
            return str(v)
        return v

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

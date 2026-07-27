from pydantic import BaseModel
from ..enlaces.models import CategoriaEnlace
from typing import Optional

#base comun
class EnlaceBase(BaseModel):
    titulo: str
    categoria: CategoriaEnlace
    url: str
    imagen_path: str


#Para crea un enlace
class EnlaceCreate(EnlaceBase):
    pass

#para actualizar
class EnlaceUpdate(EnlaceBase):
    titulo: Optional[str] = None
    categoria: Optional[CategoriaEnlace] = None
    url: Optional[str] = None
    imagen_path: Optional[str] = None


#Respuestas
class EnlaceResponse(EnlaceBase):
    id: int

    class Config:
        from_attributes = True
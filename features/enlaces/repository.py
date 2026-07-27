from features.enlaces.models import CategoriaEnlace, Enlace
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from sqlalchemy.future import select


class EnlaceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def get_all(self, categoria: CategoriaEnlace | None = None) -> Sequence[Enlace]:
        
        #aqui le digo en que tabla buscar
        query = select(Enlace)
        
        if categoria:
            # aquí puedo agregar mas filtros
            query = query.where(Enlace.categoria == categoria)
        
        result = await self.db.execute(query)
        #scalars convierte el resultado en una secuencia de objetos Enlace
        return result.scalars().all()    # all trae todos esos resultados tambien podria ser otro metodo para traer algun objeto en especifico
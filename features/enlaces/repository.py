from features.enlaces.models import CategoriaEnlace, Enlace
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from sqlalchemy.future import select
from sqlalchemy import text


class EnlaceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def seed_if_empty(self) -> None:
        query = select(Enlace)
        result = await self.db.execute(query)
        existing = result.scalars().first()
        
        if not existing:
            # Ejecutar el INSERT directamente
            insert_query = text("""
                INSERT INTO
                    enlaces (titulo, categoria, url, imagen_path)
                VALUES
                    (
                        'SIDRA Quilicura',
                        'SIDRA',
                        'https://quilicura.ssmn.cl',
                        'logos/sidra.png'
                    ),
                    (
                        'SIDRA Contingencia',
                        'SIDRA',
                        'https://contingencia.ssmn.cl',
                        'logos/sidra.png'
                    ),
                    (
                        'SIDRA Salud Norte',
                        'SIDRA',
                        'https://saludnorte.ssmn.cl',
                        'logos/sidra.png'
                    ),
                    (
                        'FONASA',
                        'OTROS',
                        'https://frontintegrado.fonasa.cl/FrontIntegradoLogin/#!/login',
                        'logos/fonasa.png'
                    ),
                    (
                        'Nobilis',
                        'OTROS',
                        'https://cesfamdequilicura.wiener-lab.com/estudios/login/?next=/estudios/',
                        'logos/nobilis.png'
                    ),
                    (
                        'HoraFacil',
                        'OTROS',
                        'https://quilicura.horafacil.cl/login',
                        'logos/horafacil.png'
                    ),
                    (
                        'OIRS',
                        'OTROS',
                        'https://oirs.minsal.cl/',
                        'logos/oirs.png'
                    ),
                    (
                        'Punto Seguro',
                        'OTROS',
                        'https://quilicurasalud.psgestion.cl/#/',
                        'logos/puntoseguro.png'
                    )
            """)
            
            await self.db.execute(insert_query)
            await self.db.commit()

            
    async def get_all(self, categoria: CategoriaEnlace | None = None) -> Sequence[Enlace]:
        
        await self.seed_if_empty()
        #aqui le digo en que tabla buscar
        query = select(Enlace)
        
        if categoria:
            # aquí puedo agregar mas filtros
            query = query.where(Enlace.categoria == categoria)
        
        result = await self.db.execute(query)
        #scalars convierte el resultado en una secuencia de objetos Enlace
        return result.scalars().all()    # all trae todos esos resultados tambien podria ser otro metodo para traer algun objeto en especifico
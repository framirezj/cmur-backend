from fastapi import APIRouter, Depends
from core.database import get_db
from .service import EnlaceService
from .repository import EnlaceRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from .schemas import EnlaceResponse, CategoriaEnlace


router = APIRouter(prefix="/enlaces",tags=["Enlaces"])


def get_service(db: AsyncSession = Depends(get_db)) -> EnlaceService:
    return EnlaceService(repo=EnlaceRepository(db=db))


@router.get("/", response_model=list[EnlaceResponse])
async def obtener_enlaces(
    categoria: Optional[CategoriaEnlace] = None,
    service: EnlaceService = Depends(get_service)    
    
):
    return await service.listar_enlaces(categoria)
    

from fastapi import APIRouter, Query
from features.indicadores.schemas import ResumenDiarioResponse
from features.indicadores.service import indicadores_service, LATITUDE_DEFAULT, LONGITUDE_DEFAULT

router = APIRouter(prefix="/indicadores", tags=["Indicadores"])


@router.get(
    "/resumen-diario",
    response_model=ResumenDiarioResponse,
    summary="Obtener resumen diario de indicadores (Temperatura, UV, Calidad del Aire, UTM)",
)
async def get_daily_summary(
    lat: float = Query(LATITUDE_DEFAULT, description="Latitud para datos climáticos"),
    lon: float = Query(LONGITUDE_DEFAULT, description="Longitud para datos climáticos"),
):
    return await indicadores_service.obtener_resumen_diario(lat, lon)

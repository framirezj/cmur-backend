from pydantic import BaseModel
from typing import Optional


class TemperaturaInfo(BaseModel):
    minima: Optional[float] = None
    maxima: Optional[float] = None
    unidad: str = "°C"


class RadiacionUVInfo(BaseModel):
    maximo_esperado: Optional[float] = None
    categoria: str


class CalidadAireInfo(BaseModel):
    pm2_5_max: Optional[float] = None
    condicion: str
    unidad: str = "µg/m³"


class UTMInfo(BaseModel):
    valor: Optional[float] = None
    unidad: str = "CLP"


class IndicadoresDetalle(BaseModel):
    temperatura: TemperaturaInfo
    radiacion_uv: RadiacionUVInfo
    calidad_aire: CalidadAireInfo
    utm: UTMInfo


class ResumenDiarioResponse(BaseModel):
    fecha: str
    indicadores: IndicadoresDetalle

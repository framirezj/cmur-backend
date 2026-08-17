from datetime import datetime
import httpx
from typing import Optional

# Santiago, Chile (Coordenadas por defecto)
LATITUDE_DEFAULT = -33.4569
LONGITUDE_DEFAULT = -70.6483


class IndicadoresService:
    def __init__(self):
        self._cache_store = {
            "date": None,  # Ej: "2026-08-17"
            "data": None,
        }

    async def obtener_resumen_diario(
        self, lat: float = LATITUDE_DEFAULT, lon: float = LONGITUDE_DEFAULT
    ) -> dict:
        today_str = datetime.now().strftime("%Y-%m-%d")

        # 1. Retornar caché si corresponde a la fecha de hoy
        if self._cache_store["date"] == today_str and self._cache_store["data"] is not None:
            return self._cache_store["data"]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        async with httpx.AsyncClient(timeout=8.0, headers=headers) as client:
            # A) UTM desde mindicador.cl
            utm_val: Optional[float] = None
            try:
                res_utm = await client.get("https://mindicador.cl/api/utm")
                if res_utm.status_code == 200:
                    data_utm = res_utm.json()
                    serie = data_utm.get("serie", [])
                    if serie:
                        utm_val = float(serie[0]["valor"])
            except Exception:
                utm_val = None

            # B) Clima y Radiación UV (Open-Meteo Forecast API)
            temp_min: Optional[float] = None
            temp_max: Optional[float] = None
            uv_max: Optional[float] = None
            try:
                url_weather = (
                    f"https://api.open-meteo.com/v1/forecast"
                    f"?latitude={lat}&longitude={lon}"
                    f"&daily=temperature_2m_max,temperature_2m_min,uv_index_max"
                    f"&timezone=auto&forecast_days=1"
                )
                res_weather = await client.get(url_weather)
                if res_weather.status_code == 200:
                    daily_weather = res_weather.json().get("daily", {})
                    if daily_weather.get("temperature_2m_min"):
                        temp_min = float(daily_weather["temperature_2m_min"][0])
                    if daily_weather.get("temperature_2m_max"):
                        temp_max = float(daily_weather["temperature_2m_max"][0])
                    if daily_weather.get("uv_index_max"):
                        uv_max = float(daily_weather["uv_index_max"][0])
            except Exception:
                pass

            # C) Calidad del Aire (Open-Meteo Air Quality API)
            pm25_max: Optional[float] = None
            calidad_texto = "No disponible"
            try:
                url_air = (
                    f"https://air-quality-api.open-meteo.com/v1/air-quality"
                    f"?latitude={lat}&longitude={lon}"
                    f"&hourly=pm2_5,pm10,european_aqi"
                    f"&forecast_days=1"
                )
                res_air = await client.get(url_air)
                if res_air.status_code == 200:
                    hourly_air = res_air.json().get("hourly", {})
                    pm25_values = [v for v in hourly_air.get("pm2_5", []) if v is not None]
                    if pm25_values:
                        pm25_max = float(max(pm25_values))

                    if pm25_max is not None:
                        if pm25_max <= 50:
                            calidad_texto = "Buena"
                        elif pm25_max <= 79:
                            calidad_texto = "Regular"
                        elif pm25_max <= 109:
                            calidad_texto = "Alerta"
                        else:
                            calidad_texto = "Preemergencia / Emergencia"
                    else:
                        calidad_texto = "Sin datos"
            except Exception:
                pass

        # Clasificación de riesgo UV diario
        if uv_max is not None:
            if uv_max < 3:
                uv_nivel = "Bajo"
            elif uv_max < 6:
                uv_nivel = "Moderado"
            elif uv_max < 8:
                uv_nivel = "Alto"
            else:
                uv_nivel = "Muy Alto"
        else:
            uv_nivel = "Sin datos"

        consolidated_data = {
            "fecha": today_str,
            "indicadores": {
                "temperatura": {
                    "minima": temp_min,
                    "maxima": temp_max,
                    "unidad": "°C",
                },
                "radiacion_uv": {
                    "maximo_esperado": uv_max,
                    "categoria": uv_nivel,
                },
                "calidad_aire": {
                    "pm2_5_max": pm25_max,
                    "condicion": calidad_texto,
                    "unidad": "µg/m³",
                },
                "utm": {
                    "valor": utm_val,
                    "unidad": "CLP",
                },
            },
        }

        # Guardar en memoria si obtenemos respuesta exitosa
        self._cache_store["date"] = today_str
        self._cache_store["data"] = consolidated_data

        return consolidated_data


# Instancia singleton del servicio para conservar el estado del caché
indicadores_service = IndicadoresService()

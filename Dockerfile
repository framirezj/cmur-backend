# Traer el ejecutable de uv desde la imagen oficial
FROM ghcr.io/astral-sh/uv:latest AS uv

# Etapa de compilación (Builder)
FROM python:3.13-slim AS builder

# Copiar el binario de uv
COPY --from=uv /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

# Instalar dependencias antes de copiar el código para aprovechar la caché de Docker
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copiar el código del proyecto y sincronizar el proyecto completo
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Etapa final (Ejecución)
FROM python:3.13-slim
WORKDIR /app

# Copiar el entorno virtual compilado y el código
COPY --from=builder /app/.venv /app/.venv
COPY . /app

# Asegurar que los ejecutables del entorno virtual estén en el PATH
ENV PATH="/app/.venv/bin:$PATH"

# Exponer el puerto por defecto de FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación en modo producción
CMD ["fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]

from fastapi import HTTPException, status
from features.usuarios.models import Usuario
from features.usuarios.repository import UsuarioRepository
from core.security import verify_google_token, create_access_token
from features.enlaces.storage import storage_service


class UsuarioService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    # ── Auth ──────────────────────────────────────────────────────────────────

    async def login_con_google(self, id_token_str: str) -> dict:
        """
        Valida el id_token de Google, crea el usuario si no existe
        y retorna el JWT propio junto con los datos del usuario.
        """
        # 1. Verificar el token con Google
        try:
            payload = verify_google_token(id_token_str)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
            )

        google_sub = payload["sub"]
        email = payload.get("email", "")
        nombre = payload.get("name", email)
        foto_url = payload.get("picture")

        # 2. Buscar o crear al usuario
        usuario = await self.repo.get_by_google_sub(google_sub)
        if not usuario:
            usuario = await self.repo.crear(
                Usuario(
                    google_sub=google_sub,
                    nombre=nombre,
                    email=email,
                    foto_url=foto_url,
                )
            )

        # 3. Emitir JWT propio (sub = usuario.id)
        access_token = create_access_token({"sub": str(usuario.id)})

        return {"access_token": access_token, "usuario": usuario}

    # ── Perfil ────────────────────────────────────────────────────────────────

    async def obtener_usuario(self, usuario_id: int) -> Usuario:
        usuario = await self.repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return usuario

    # ── Favoritos ─────────────────────────────────────────────────────────────

    async def listar_favoritos(self, usuario_id: int):
        """Retorna los favoritos del usuario con las URLs de imagen resueltas."""
        favoritos = await self.repo.get_favoritos(usuario_id)
        for fav in favoritos:
            fav.enlace.imagen_path = storage_service.get_url(fav.enlace.imagen_path)
        return favoritos

    async def agregar_favorito(self, usuario_id: int, enlace_id: int):
        # Verificar que el enlace existe
        enlace = await self.repo.get_enlace_by_id(enlace_id)
        if not enlace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enlace no encontrado")

        # Verificar que no está ya en favoritos
        if await self.repo.favorito_existe(usuario_id, enlace_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El enlace ya está en favoritos")

        favorito = await self.repo.agregar_favorito(usuario_id, enlace_id)
        favorito.enlace.imagen_path = storage_service.get_url(favorito.enlace.imagen_path)
        return favorito

    async def eliminar_favorito(self, usuario_id: int, enlace_id: int):
        eliminado = await self.repo.eliminar_favorito(usuario_id, enlace_id)
        if not eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorito no encontrado")

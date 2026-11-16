from fastapi import HTTPException, status
from features.usuarios.models import Usuario
from features.usuarios.repository import UsuarioRepository
from features.usuarios.schemas import RegistroRequest, LoginRequest
from core.security import hash_pin, verify_pin, create_access_token
from features.enlaces.storage import storage_service


class UsuarioService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    # ── Auth ──────────────────────────────────────────────────────────────────

    async def registrar(self, data: RegistroRequest) -> dict:
        """
        Registra un nuevo funcionario con PIN de 4 dígitos.
        Por defecto se le asigna el rol 'usuario'.
        """
        # 1. Verificar si el RUT ya existe
        usuario_existente = await self.repo.get_by_rut(data.rut)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El RUT ya se encuentra registrado",
            )

        # 2. Verificar email si fue proporcionado
        if data.email:
            email_existente = await self.repo.get_by_email(data.email)
            if email_existente:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El correo electrónico ya se encuentra registrado",
                )

        # 3. Hashear el PIN de 4 dígitos
        pin_hasheado = hash_pin(data.pin)

        # 4. Crear el usuario con rol 'usuario'
        nuevo_usuario = Usuario(
            rut=data.rut,
            nombre=data.nombre,
            pin_hash=pin_hasheado,
            rol="usuario",
            email=data.email,
        )
        usuario = await self.repo.crear(nuevo_usuario)

        # 5. Emitir JWT propio con sub y rol
        access_token = create_access_token({"sub": str(usuario.id), "rol": usuario.rol})

        return {"access_token": access_token, "token_type": "bearer", "usuario": usuario}

    async def login(self, data: LoginRequest) -> dict:
        """
        Inicia sesión mediante RUT y PIN de 4 dígitos.
        Retorna el JWT propio junto con los datos del usuario.
        """
        usuario = await self.repo.get_by_rut(data.rut)
        if not usuario or not verify_pin(data.pin, usuario.pin_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="RUT o PIN incorrecto",
            )

        access_token = create_access_token({"sub": str(usuario.id), "rol": usuario.rol})
        return {"access_token": access_token, "token_type": "bearer", "usuario": usuario}

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

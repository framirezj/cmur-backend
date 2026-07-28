from features.enlaces.repository import EnlaceRepository
from features.enlaces.storage import storage_service


class EnlaceService:
    def __init__(self, repo: EnlaceRepository):
        self.repo = repo

    #listas los enlaces
    async def listar_enlaces(self, categoria=None):
        enlaces = await self.repo.get_all(categoria)
        for enlace in enlaces:
            enlace.imagen_path = storage_service.get_url(enlace.imagen_path)

        return enlaces
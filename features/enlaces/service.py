from features.enlaces.repository import EnlaceRepository



class EnlaceService:
    def __init__(self, repo: EnlaceRepository):
        self.repo = repo

    #listas los enlaces
    async def listar_enlaces(self, categoria=None):
        return await self.repo.get_all(categoria)
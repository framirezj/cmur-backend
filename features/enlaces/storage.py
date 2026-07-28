from core.config import settings


class StorageService:
    def __init__(self):
        self.api_url = settings.API_URL.rstrip("/")

    
    def get_url(self, reference: str):
        return f"{self.api_url}/{reference}"

    
    
storage_service = StorageService()
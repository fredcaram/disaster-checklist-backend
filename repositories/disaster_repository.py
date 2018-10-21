from repositories.base_repository import BaseRepository

class DisasterRepository(BaseRepository):
    Model = None

    def __init__(self):
        super().__init__("disasters")
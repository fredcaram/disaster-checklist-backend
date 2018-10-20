from repositories.base_repository import BaseRepository

class ItemRepository(BaseRepository):
    def __init__(self):
        super().__init__("items")
from repositories.base_repository import BaseRepository, DEFAULT_GET_COLLECTION_PATH
from firebase_admin import db

class ItemRepository(BaseRepository):
    def __init__(self):
        super().__init__("items")

    def get_items(self, items_ids):
        database_ref = db.reference(DEFAULT_GET_COLLECTION_PATH.format(self._database_name))
        items = [database_ref.order_by_key().equal_to(item_id) for item_id in items_ids]
        return items
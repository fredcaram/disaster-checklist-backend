from repositories.base_repository import BaseRepository, DEFAULT_GET_COLLECTION_PATH
from firebase_admin import db
import numpy as np
import pandas

class ItemRepository(BaseRepository):
    def __init__(self):
        super().__init__("items")

    def get_items(self, items_ids):
        database_ref = db.reference(DEFAULT_GET_COLLECTION_PATH.format(self._database_name))

        items = []
        for item_id in items_ids:
            item = dict(database_ref.order_by_child("item_id").equal_to(item_id).get())
            item_values = item.values()
            items += item_values
        items_df = pandas.DataFrame(items)

        return items_df.to_dict(orient="row")
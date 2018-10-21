from repositories.base_repository import BaseRepository
from recommender import recommender_list
from firebase_admin import db


import pandas as pd

class ListRepository(BaseRepository):
    Model = None

    def __init__(self):
        super().__init__("list_items")

    def get_list_for_disaster(self, user_profile_df:pd.DataFrame, disaster_id):
        model = self._get_model()
        list_items = model.predict(user_data=user_profile_df, id_category=disaster_id)
        return list_items


    def _get_model(self):
        if ListRepository.Model is None:
            ListRepository.Model = recommender_list.load_model()

        return ListRepository.Model


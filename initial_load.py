from repositories.user_repository import UserRepository
from repositories.item_repository import ItemRepository
import csv
import json
import pandas as pd

from firebase_initializer import initialize_firebase

initialize_firebase()

def load_items():
    file_name = "initial_load/item_list.csv"
    with open(file_name) as f:
        item_df = pd.read_csv(f)
        item_list = item_df.to_dict(orient="row")
        item_repo = ItemRepository()

        for item in item_list:
            item_repo.add(item)


def load_users():
    file_name = "initial_load/sample_users.csv"
    with open(file_name) as f:
        user_df = pd.read_csv(f)
        user_list = user_df.to_dict(orient="row")
        user_repo = UserRepository()

        for user in user_list:
            user_repo.add(user)


load_items()
load_users()
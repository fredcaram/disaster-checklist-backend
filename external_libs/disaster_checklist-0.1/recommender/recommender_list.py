import pandas as pd
import numpy as np
from sklearn import preprocessing
from scipy.spatial.distance import cdist
import category_encoders as ce
from os import path
from pathlib import Path


class ListItems(object):
    def __init__(self, user_data: pd.DataFrame):
        self.user_data = user_data

    def users_list(self, user_ids, category_id) -> pd.DataFrame:

        query = "idUser in [{user_id}] & idCategory == {category}".format(user_id=",".join(map(str, user_ids)),
                                                                        category=category_id)
        return self.user_data.query(query)


class UserModel(object):
    COLUMNS_TO_DROP = ['id', 'name', 'email', 'phone', 'home', 'neighborhood', 'location']

    CATEGORIES = ['sex', 'city', 'petOwner', 'reducedMobility',
                  'practiceSports', 'smoker', 'drinker', 'mainHobby', 'carOwner', 'currentJob', 'motherLanguage']

    NORMALIZE = ['age', 'children', 'weigth', 'height', 'yearIncome']
    ALL_COLUMNS = ['sex', 'age', 'city', 'children', 'reducedMobility', 'carOwner', 'weight',
                   'height', 'practiceSports', 'smoker', 'drinker', 'yearIncome', 'currentJob', 'mainHobby',
                   'motherLanguage', 'petOwner']

    encoders = {}
    normalizers = {}
    user_ids = None

    def __init__(self, user_data: pd.DataFrame, list_items: ListItems, K=5):
        """

        :param user_data: User profiles to use on train
        :param K: number of neighbors to use
        """
        self.K = K
        self.list_items = list_items
        self.user_ids = user_data.id.values
        # Remove used columns
        user_data.drop(columns=UserModel.COLUMNS_TO_DROP, inplace=True, errors='ignore')

        user_data = self.__encode(user_data, fit=True)
        user_data = self.__normalize(user_data, fit=True)
        self.U = user_data.values

    def __encode(self, user_data: pd.DataFrame, fit=False) -> pd.DataFrame:
        """
        Encode inplace the columns of a user.
        :param user_data: User profile that will be encoded inplace
        :param fit: if True the encoder will be fitted otherwise it'll use a already trained encoder
        :return: None
        """
        if fit:
            self.encoders = {}
            enc = ce.BinaryEncoder(cols=UserModel.CATEGORIES)
            for c in UserModel.CATEGORIES:
                if c not in user_data:
                    user_data[c] = ""

            self.encoders['bin'] = enc.fit(user_data)

        for c in UserModel.CATEGORIES:
            if c not in user_data:
                user_data[c] = ""
        user_data = self.encoders['bin'].transform(user_data)
        return user_data

    def __normalize(self, user_data: pd.DataFrame, fit=False) -> pd.DataFrame:
        """
        Normalize a user profile
        :param user_data:
        :param fit:
        :return:
        """
        if fit:
            self.normalizers = {}

        for c in UserModel.NORMALIZE:
            if fit:
                norm = preprocessing.MinMaxScaler()
                if c not in user_data:
                    user_data[c] = 0
                self.normalizers[c] = norm.fit(user_data[[c]].values)

            if c not in user_data:
                user_data[c] = 0

            user_data[[c]] = self.normalizers[c].transform(user_data[[c]].values)

        return user_data

    def predict(self, user_data: pd.DataFrame, id_category, top=0) -> pd.DataFrame:
        """

        :param user_data: User profile
        :param id_category: category to recommende
        :param top: limit the size of the list
        :return: list with items and relevance
        """
        user_data.drop(user_data.columns.difference(UserModel.ALL_COLUMNS), 1, inplace=True, errors='ignore')
        user_data = self.__encode(user_data, fit=False)
        user_data = self.__normalize(user_data, fit=False)

        # Select
        rank = cdist(self.U, user_data.values, metric='cosine')
        r = np.array([r[0] for r in rank])
        index = r.argsort()[-self.K:][::-1]

        user_ids = [self.user_ids[i] for i in index]
        items = self.list_items.users_list(user_ids, id_category)
        group = items.groupby('idItem').size().reset_index(name='counts')
        group.sort_values('counts', ascending=False, inplace=True)
        if top > 0:
            group = group.head(top)

        group.rename({'counts': 'FREQUENCY'}, axis=1, inplace=True)
        return group


def load_model():
    rootpath = Path(path.dirname(__file__))

    user_profile_with_lists = rootpath / 'data/user_data2.csv'
    user_lists = rootpath / 'data/user_itens.csv'
    user_items = pd.read_csv(user_lists, sep='\t')

    user_data = pd.read_csv(user_profile_with_lists, sep=";")
    list_items = ListItems(user_items)
    user_model = UserModel(user_data.copy(), list_items)

    return user_model

#"""
if __name__ == "__main__":
    import pickle

    user_profile_with_lists = 'data/user_data2.csv'
    user_lists = 'data/user_itens.csv'
    user_items = pd.read_csv(user_lists, sep='\t')

    user_data = pd.read_csv(user_profile_with_lists, sep=";")
    list_items = ListItems(user_items)
    user_model = UserModel(user_data.copy(), list_items)
    pickle.dump(user_model, open("user_model.pkl", "wb"))
#"""

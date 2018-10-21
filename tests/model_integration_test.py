from recommender import recommender_list
from repositories.user_repository import UserRepository
from firebase_initializer import initialize_firebase
import pandas as pd

initialize_firebase()
user_repo = UserRepository()
user_profile = user_repo.get("-LPIy7P5NJTaRPQcGiLw")
user_profile_df = pd.DataFrame(user_profile, index=[user_profile["id"]])

print(list(user_profile_df.columns))
model = recommender_list.load_model()
new_list = model.predict(user_data=user_profile_df, id_category=1)
print(new_list)

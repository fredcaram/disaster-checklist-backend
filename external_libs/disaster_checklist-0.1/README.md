# The end is near recommender
```
python3 -m venv venv
source venv/bin/acitvate
pip install -r requirements.txt
python setup.py sdist
```

How to use
```python
from recommender import recommender_list
model = recommender_list.load_model()
new_list = model.predict(user_data=user_profile, id_category=ID_DISASTER)

```

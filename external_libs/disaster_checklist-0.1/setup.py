from setuptools import setup

setup(name='disaster_checklist',
      version='0.1',
      package_data={'recommender': ['data/*.csv']},
      description='',
      author='Evandro',
      author_email='ecaldeira@avenuecode.com',
      license='MIT',
      packages=['recommender'])
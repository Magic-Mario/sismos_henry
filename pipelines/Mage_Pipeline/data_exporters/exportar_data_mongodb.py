from os import path

from pandas import DataFrame

from pymongo import MongoClient

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.mongodb import MongoDB

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
#test
@data_exporter
def export_data_to_mongodb(df: DataFrame, **kwargs) -> None:
    connection_string = "mongodb+srv://copito:golazo@cluster1.krfn9qj.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Sismos"]
    collection = db["prueba"]
    collection.insert_many(df.to_dict('records'))
   

    



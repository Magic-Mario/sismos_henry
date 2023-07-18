if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def remove_duplicates_custom(data, *args, **kwargs):
    """
    Args:
        data: The output from the upstream parent block (if applicable)
        args: The output from any additional upstream blocks

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Importar las bibliotecas necesarias
    from pymongo import MongoClient

    # Establecer la conexión a MongoDB
    connection_string = "mongodb+srv://<username>:<password>@<cluster_address>/<database>?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client["<database_name>"]
    collection = db["<collection_name>"]

    # Eliminar registros duplicados en MongoDB
    pipeline = [
        {"$group": {"_id": <group_id>, "duplicates": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}},
        {"$project": {"duplicates": {"$slice": ["$duplicates", 1, {"$size": "$duplicates"}]}}}
    ]
    duplicate_ids = list(collection.aggregate(pipeline))
    for duplicate in duplicate_ids:
        collection.delete_many({"_id": {"$in": duplicate["duplicates"]}})

    # Cerrar la conexión a MongoDB
    client.close()

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
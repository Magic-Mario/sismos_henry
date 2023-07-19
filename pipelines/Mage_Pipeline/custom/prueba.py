from pymongo import MongoClient
from mage_ai.data_preparation.decorators import custom

@custom
def remove_duplicates(data, **kwargs):
    connection_string = "mongodb+srv://copito:golazo@cluster1.krfn9qj.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["10"]
    collection = db["1"]

    # Find duplicate documents based on a specific field
    pipeline = [
        {"$group": {"_id": "$field_name", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    duplicates = list(collection.aggregate(pipeline))

    # Remove duplicate documents
    for duplicate in duplicates:
        field_value = duplicate["_id"]
        collection.delete_many({"field_name": field_value})

# Call the remove_duplicates function
remove_duplicates(df)
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("MONGODB_PASSWORD")

#print(password)

uri = f"mongodb+srv://picassojp:{password}@cluster0.cchanol.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

db = client["pf-henry"]
collection = db["db-pf-henry"]

result = collection.find_one()  # Retrieves a single document from the collection


cursor = collection.find()  # Obtiene un cursor para recorrer los documentos


# Close the MongoDB connection
client.close()
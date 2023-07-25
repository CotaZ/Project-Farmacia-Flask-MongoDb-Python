from pymongo import MongoClient
import certifi
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = #Conecta tu base de datos Mongo Atlas
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client['farmacia']
    except ServerSelectionTimeoutError as e:
        raise ConnectionError("Error al conectar con la base de datos") from e
    return db

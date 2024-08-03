from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client2 = MongoClient(connection_string)

session2 = client2.start_session()
session2.start_transaction(
    read_concern=ReadConcern("local"),
    read_preference=ReadPreference.PRIMARY
)

db = client2['negozio_abbigliamento']
capiCollection = db['capi_abbigliamento']
capo_id = 1

doc = capiCollection.find_one({'capoId': capo_id}, session=session2)
print(doc)
initial_price = doc.get("prezzo").to_decimal()
print("Prezzo del capo: ", initial_price)

session2.commit_transaction()
session2.end_session()
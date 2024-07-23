import time

from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

client2 = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

session2 = client2.start_session()
session2.start_transaction(
    read_concern=ReadConcern("local"),
    read_preference=ReadPreference.PRIMARY
)

db = client2['negozio_abbigliamento']
myCollection = db['capi_abbigliamento']
id = 1


for i in range(0,2):
    doc = myCollection.find_one({'_id': id}, session=session2)
    print(doc)
    price = doc.get("prezzo")
    print("Prezzo: ", price, "\n")
    time.sleep(5)


session2.commit_transaction()
session2.end_session()
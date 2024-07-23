from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

client2 = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

session2 = client2.start_session()
session2.start_transaction(
    read_concern=ReadConcern("majority"),
    write_concern=WriteConcern("majority"),
)

db = client2['sample_analytics']
myCollection = db['collection_prova']

doc = myCollection.find_one({'_id': '1'}, session=session2);
initial_price = doc.get("price");
print("T2 - Prezzo iniziale: ", initial_price);

time.sleep(10)

try:
    myCollection.update_one({'_id': '1'}, {'$inc': {'price': 10}}, session=session2)
    modified_doc = myCollection.find_one({'_id': '1'}, session=session2);
    final_price = modified_doc.get("price");
    print("T2 - Prezzo finale: ", final_price);
    session2.commit_transaction()
except Exception as e:
    print(f"Errore durante l'aggiornamento: {e}")

session2.end_session()

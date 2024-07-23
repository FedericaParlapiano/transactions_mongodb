from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time


client1 = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

session1 = client1.start_session()
session1.start_transaction(
    read_concern=ReadConcern("majority"),
    write_concern=WriteConcern("majority"),
)


db = client1['sample_analytics']
myCollection = db['collection_prova']

doc = myCollection.find_one({'_id': '1'}, session=session1);
initial_price = doc.get("price");
print("T1 - Prezzo iniziale: ", initial_price);

time.sleep(5)

myCollection.update_one({'_id': '1'}, {'$inc': {'price': 10}}, session=session1)

modified_doc = myCollection.find_one({'_id': '1'}, session=session1);
final_price = modified_doc.get("price");
print("T1 - Prezzo finale: ", final_price);

time.sleep(5)

try:
    session1.commit_transaction()
except Exception as e:
    print(f"Errore durante il commit della transazione: {e}")

session1.end_session()

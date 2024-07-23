from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

client2 = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

session2 = client2.start_session()
session2.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern("majority"),
)

db = client2['negozio_abbigliamento']
myCollection = db['capi_abbigliamento']
id = 1

doc = myCollection.find_one({'_id': id}, session=session2);
print("Documento da modificare: ", doc)
initial_price = doc.get("prezzo");
print("Prezzo iniziale: ", initial_price);

time.sleep(3)

try:
    myCollection.update_one({'_id': id}, {'$inc': {'prezzo': 10}}, session=session2)

    modified_doc = myCollection.find_one({'_id': id}, session=session2);
    final_price = modified_doc.get("prezzo");
    print("Documento modificato: ", modified_doc)
    print("Prezzo finale: ", final_price);

except Exception as e:
    print(f"Errore durante l'aggiornamento: {e}")

try:
    session2.commit_transaction()
    print("Transazione andata a buon fine.");
except Exception as e:
    print(f"Errore durante il commit della transazione: {e}")

session2.end_session()

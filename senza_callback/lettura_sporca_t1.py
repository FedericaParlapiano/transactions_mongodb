from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

import time


connection_string = "..."
client1 = MongoClient(connection_string)

session1 = client1.start_session()
session1.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern(w=1, j=False),
    read_preference=ReadPreference.PRIMARY
)


db = client1['negozio_abbigliamento']
capiCollection = db['capi_abbigliamento']
capo_id = 1
additional_price = 5

doc = capiCollection.find_one({'capoId': capo_id}, {'_id': False}, session=session1)
print(doc)
initial_price = doc.get("prezzo").to_decimal()
print("Prezzo iniziale: ", initial_price)

try:
    capiCollection.update_one({'capoId': capo_id}, {"$set": {"prezzo": Decimal128(initial_price + additional_price)}}, session=session1)

    modified_doc = capiCollection.find_one({'capoId': capo_id}, {'_id': False}, session=session1)
    final_price = modified_doc.get("prezzo").to_decimal()
    print("Documento modificato: ", modified_doc)
    print("Prezzo finale: ", final_price)
except Exception as e:
    print(f"Errore durante l'aggiornamento: {e}")

time.sleep(10)

session1.abort_transaction()
print("\nTransazione abortita.")

session1.end_session()
client1.close()

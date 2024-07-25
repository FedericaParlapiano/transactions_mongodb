from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time


client1 = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

session1 = client1.start_session()
session1.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern("majority"),
)


db = client1['negozio_abbigliamento']
myCollection = db['capi_abbigliamento']
id = 1

doc = myCollection.find_one({'_id': id}, session=session1);
print("Documento da modificare: ", doc)
initial_price = doc.get("prezzo");
print("Prezzo iniziale: ", initial_price);

time.sleep(3)

try:
    myCollection.update_one({'_id': id}, {"$set": { "prezzo": round(float(initial_price-10), 2) }}, session=session1)

    modified_doc = myCollection.find_one({'_id': id}, session=session1);
    final_price = modified_doc.get("prezzo");
    print("\n\nDocumento modificato: ", modified_doc)
    print("Prezzo finale: ", final_price);

    try:
        session1.commit_transaction()
        print("\n\nTransazione andata a buon fine.\n");

    except Exception as e:
        print(f"\n\nErrore durante il commit della transazione: {e.__cause__}")
        session1.abort_transaction()

except Exception as e:
    print(f"\n\nErrore durante l'aggiornamento: {e.__cause__}")
    print("\n\nTransazione abortita. \n")

session1.end_session()

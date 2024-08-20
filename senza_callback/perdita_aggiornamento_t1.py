from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time


connection_string = "..."
client1 = MongoClient(connection_string)

session1 = client1.start_session()
session1.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern("majority"),
)


db = client1['negozio_abbigliamento']
myCollection = db['capi_abbigliamento']
capo_id = 1
additional_price = 10

doc = myCollection.find_one({'capoId': capo_id}, session=session1)
print("Documento da modificare: ", doc)
initial_price = doc.get("prezzo").to_decimal()
print("Prezzo iniziale: ", initial_price)

time.sleep(3)

try:
    myCollection.update_one({'capoId': capo_id},
                            {"$set": {"prezzo": Decimal128(initial_price + additional_price)}},
                            session=session1)

    modified_doc = myCollection.find_one({'capoId': capo_id}, session=session1);
    final_price = modified_doc.get("prezzo").to_decimal()
    print("\n\nDocumento modificato: ", modified_doc)
    print("Prezzo finale: ", final_price)

    try:
        session1.commit_transaction()
        print("\n\nTransazione andata a buon fine.\n")

    except Exception as e:
        print(f"\n\nErrore durante il commit della transazione: {e.__cause__}")
        session1.abort_transaction()

except Exception as e:
    print(f"\n\nErrore durante l'aggiornamento: {e.args[0]}")
    print("\nTransazione abortita. \n")
    session1.abort_transaction()


session1.end_session()
client1.close()

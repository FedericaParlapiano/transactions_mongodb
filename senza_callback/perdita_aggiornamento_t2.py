from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time


connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client2 = MongoClient(connection_string)

session2 = client2.start_session()
session2.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern("majority"),
)


db = client2['negozio_abbigliamento']
myCollection = db['capi_abbigliamento']
capo_id = 1
additional_price = 10

doc = myCollection.find_one({'capoId': capo_id}, session=session2)
print("Documento da modificare: ", doc)
initial_price = doc.get("prezzo").to_decimal()
print("Prezzo iniziale: ", initial_price)

time.sleep(3)

try:
    myCollection.update_one({'capoId': capo_id},
                            {"$set": {"prezzo": Decimal128(initial_price + additional_price)}},
                            session=session2)

    modified_doc = myCollection.find_one({'capoId': capo_id}, session=session2);
    final_price = modified_doc.get("prezzo").to_decimal()
    print("\n\nDocumento modificato: ", modified_doc)
    print("Prezzo finale: ", final_price)

    try:
        session2.commit_transaction()
        print("\n\nTransazione andata a buon fine.\n")

    except Exception as e:
        print(f"\n\nErrore durante il commit della transazione: {e.__cause__}")
        session2.abort_transaction()

except Exception as e:
    print(f"\n\nErrore durante l'aggiornamento: {e.args[0]}")
    print("\nTransazione abortita. \n")
    session2.abort_transaction()


session2.end_session()
client2.close()
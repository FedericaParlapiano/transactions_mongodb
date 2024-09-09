import time

from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

connection_string = "..."
client2 = MongoClient(connection_string)

session2 = client2.start_session()
session2.start_transaction(
    read_concern=ReadConcern(level="local"),
    write_concern=WriteConcern(w=1, j=False),
)

db = client2['negozio_abbigliamento']
capiCollection = db['capi_abbigliamento']
capo_id = 1
additional_price = 10

try:
    doc = capiCollection.find_one(
        {'capoId': capo_id},
        {'_id': False},
        session=session2,
    )
    print("Documento da modificare: ", doc)
    initial_price = doc.get("prezzo").to_decimal()
    print("Prezzo iniziale: ", initial_price)
    capiCollection.update_one({'capoId': capo_id}, {"$set": {"prezzo": Decimal128(initial_price + additional_price)}}, session=session2)

    modified_doc = capiCollection.find_one({'capoId': capo_id}, {'_id': False}, session=session2)
    final_price = modified_doc.get("prezzo").to_decimal()
    print("\nDocumento modificato: ", modified_doc)
    print("Prezzo finale: ", final_price)

    time.sleep(2)

    try:
        session2.commit_transaction()
        print("\n\nTransazione andata a buon fine.\n")

    except Exception as e:
        print(f"\n\nErrore durante l'aggiornamento: {e.args[0]}")
        print("\nTransazione abortita.\n")
        session2.abort_transaction()

except Exception as e:
    print(f"Errore durante l'aggiornamento: {e.args[0]}")

session2.end_session()
client2.close()

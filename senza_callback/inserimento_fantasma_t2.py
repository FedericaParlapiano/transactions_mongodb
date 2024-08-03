import pprint

from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time


client2 = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

session2 = client2.start_session()
session2.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern(w=1, j=False),
)


db = client2['negozio_abbigliamento']
capiCollection = db['capi_abbigliamento']
colore = "rosso"


cursor = capiCollection.find({'colore': colore}, {'_id': False}, session=session2)
print(f"Articoli di colore {colore}.")
num_docs = 0
for document in cursor:
    num_docs += 1
    pprint.pprint(document)
    print()
print(f"Numero dei capi di colore {colore}: {str(num_docs)}.\n")
try:
    capiCollection.insert_one({"nome": "Maglione", "prezzo": Decimal128("59.99"), "colore": "rosso",
                               "disponibilita": {"S": 30, "M": 50, "L": 20}})
    print(f"Inserimento di un nuovo articolo di colore {colore}.\n")

except Exception as e:
    print(f"Errore durante l'inserimento dell'articolo: {e.args[0]}")

try:
    session2.commit_transaction()
    print("Transazione andata a buon fine.\n\n")

    print(f"Articoli di colore {colore}.")
    cursor = capiCollection.find({'colore': colore}, session=session2)
    num_docs = 0
    for document in cursor:
        num_docs += 1
        pprint.pprint(document)
        print()
    print(f"Numero dei capi di colore {colore}: {str(num_docs)}.")

except Exception as e:
    print(f"Errore durante il commit della transazione: {e.args[0]}")
    session2.abort_transaction()

session2.end_session()
client2.close()

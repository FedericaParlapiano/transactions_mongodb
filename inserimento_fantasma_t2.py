import pprint

from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time


client1 = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

session2 = client1.start_session()
session2.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern(1),
)


db = client1['negozio_abbigliamento']
myCollection = db['capi_abbigliamento']
colore = "rosso"


cursor = myCollection.find({'colore': colore}, session=session2);
print(f"Articoli di colore {colore}.")
num_docs = 0
for document in cursor:
    num_docs += 1
    pprint.pprint(document)
    print()
print(f"Numero dei capi di colore {colore}: {str(num_docs)}.\n\n")
try:
    myCollection.insert_one({"_id": 11, "nome": "Maglione", "prezzo": 59.99, "colore": "rosso", "taglia": "M", "quantità": 20})
    print(f"Inserimento di un nuovo articolo di colore {colore}.\n")

except Exception as e:
    print(f"Errore durante l'inserimento dell'articolo: {e}")

try:
    session2.commit_transaction()
    print("Transazione andata a buon fine.\n\n")

    print(f"Articoli di colore {colore}.")
    cursor = myCollection.find({'colore': colore}, session=session2);
    num_docs = 0
    for document in cursor:
        num_docs += 1
        pprint.pprint(document)
        print()
    print(f"Numero dei capi di colore {colore}: {str(num_docs)}.")

except Exception as e:
    print(f"Errore durante il commit della transazione: {e}")
    session2.abort_transaction()



session2.end_session()

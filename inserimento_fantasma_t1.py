import pprint

from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time


client1 = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

session1 = client1.start_session()
session1.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern(1),
)


db = client1['negozio_abbigliamento']
myCollection = db['capi_abbigliamento']
colore = "rosso"

for i in range(0,2):
    print(f"Articoli di colore {colore}.")
    cursor = myCollection.find({'colore': colore}, session=session1);
    num_docs = 0
    for document in cursor:
        num_docs += 1
        pprint.pprint(document)
        print()
    print(f"Numero dei capi di colore {colore}: {str(num_docs)}\n")
    time.sleep(5)

try:
    session1.commit_transaction()

except Exception as e:
    print(f"Errore durante il commit della transazione: {e}")
    session1.abort_transaction()

session1.end_session()

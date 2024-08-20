import pprint

from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time


connection_string = "..."
client1 = MongoClient(connection_string)


session1 = client1.start_session()
session1.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern(w=1, j=False),
)

db = client1['negozio_abbigliamento']
capiCollection = db['capi_abbigliamento']
colore = "rosso"

for i in range(0,2):
    print(f"Articoli di colore {colore}.")
    cursor = capiCollection.find({'colore': colore}, {'_id': False}, session=session1);
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
client1.close()

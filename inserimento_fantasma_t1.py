import pprint
import time

from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from pymongo.read_concern import ReadConcern

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client = MongoClient(connection_string)

def callback(session, colore):
    capiCollection = session.client.negozio_abbigliamento.capi_abbigliamento.with_options(
        write_concern=WriteConcern(w=1, j=False)
    )

    for i in range(0,2):
        print(f"Articoli di colore {colore}.")
        cursor = capiCollection.find({'colore': colore}, {'_id': False}, session=session)
        num_docs = 0
        for document in cursor:
            num_docs += 1
            pprint.pprint(document)
            print()
        print(f"Numero dei capi di colore {colore}: {str(num_docs)}\n")
        time.sleep(5)

    try:
        session.commit_transaction()

    except Exception as e:
        print(f"Errore durante il commit della transazione: {e}")
        session.abort_transaction()

def callback_wrapper(s):
    callback(
        session=s,
        colore="rosso"
    )


with client.start_session() as session:
    try:
        session.with_transaction(
            callback_wrapper,
            read_concern=ReadConcern(level="local"),
            write_concern=WriteConcern(w=1, j=False)
        )
    except PyMongoError as e:
        print(f"Transazione fallita: {e.args[0]}")

client.close()

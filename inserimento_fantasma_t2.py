import pprint

from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from pymongo.read_concern import ReadConcern

connection_string = "..."
client = MongoClient(connection_string)

def callback(session, colore):
    capiCollection = session.client.negozio_abbigliamento.capi_abbigliamento.with_options(
        write_concern=WriteConcern(w=1, j=False)
    )


    cursor = capiCollection.find({'colore': colore}, {'_id': False}, session=session)
    print(f"Articoli di colore {colore}.")
    num_docs = 0
    for document in cursor:
        num_docs += 1
        pprint.pprint(document)
        print()
    print(f"Numero dei capi di colore {colore}: {str(num_docs)}.\n\n")
    try:
        capiCollection.insert_one({"nome": "Maglione", "prezzo": Decimal128("59.99"), "colore": "rosso", "disponibilita": {"S": 30, "M": 50, "L": 20}})
        print(f"Inserimento di un nuovo articolo di colore {colore}.\n")

    except Exception as e:
        print(f"Errore durante l'inserimento dell'articolo: {e.args[0]}")

    try:
        session.commit_transaction()
        print("Transazione andata a buon fine.\n\n")

        print(f"Articoli di colore {colore}.")
        cursor = capiCollection.find({'colore': colore}, session=session)
        num_docs = 0
        for document in cursor:
            num_docs += 1
            pprint.pprint(document)
            print()
        print(f"Numero dei capi di colore {colore}: {str(num_docs)}.")

    except Exception as e:
        print(f"Errore durante il commit della transazione: {e.args[0]}")
        session.abort_transaction()

def callback_wrapper(s):
    colore = "rosso"
    callback(
        session=s,
        colore=colore
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

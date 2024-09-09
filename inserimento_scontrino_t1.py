from datetime import datetime

from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from pymongo.read_concern import ReadConcern
import time

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client1 = MongoClient(connection_string)


def callback(session, capi, taglie):
    capiCollection = session.client.negozio_abbigliamento.capi_abbigliamento.with_options(
        write_concern=WriteConcern(w=1, j=False)
    )
    scontriniCollection = session.client.negozio_abbigliamento.scontrini.with_options(
        write_concern=WriteConcern(w=1, j=False)
    )

    articoli = []
    totale_complessivo = 0

    print("")
    try:
        for capo, taglia in zip(capi, taglie):
            articolo = capiCollection.find_one({'nome': capo}, {'_id': False}, session=session)
            prezzo_articolo = articolo.get("prezzo").to_decimal()

            print(f"Tentativo di acquisto di {articolo.get('nome')} (taglia: {taglia}) con ID {articolo.get('capoId')}")
            print(articolo)

            time.sleep(3)

            capiCollection.update_one({'nome': capo}, {'$inc': {f'disponibilita.{taglia}': -1}}, session=session)
            articolo_aggiornato = capiCollection.find_one({'nome': capo}, {'_id': False},  session=session)
            print(f"Aggiornamento quantità: {articolo_aggiornato}\n")

            articoli.append({"nome": capo, "quantita": 1, "prezzo_totale": Decimal128(str(prezzo_articolo)), "taglia": taglia})
            totale_complessivo += prezzo_articolo

        totale_complessivo = Decimal128(str(totale_complessivo))

        nuovo_scontrino = {
            "data": datetime.strptime(str(datetime.now().date()), "%Y-%m-%d"),
            "articoli": articoli,
            "totale_complessivo": totale_complessivo
        }

        scontriniCollection.insert_one(nuovo_scontrino)
        print("Acquisto terminato.")
        print(f"Scontrino: {nuovo_scontrino}\n")
        time.sleep(4)
        session.commit_transaction()
        print("Transazione andata a buon fine.\n")
        time.sleep(3)

    except Exception as e:
        print(f"\n\nErrore durante la transazione: {e.args[0]}")
        print("\n\nTransazione abortita. \n")


def callback_wrapper(s):
    capi = ["Cappotto"]
    taglie = ["M"]
    callback(
        session=s,
        capi=capi,
        taglie=taglie
    )


with client1.start_session() as session:
    try:
        session.with_transaction(
            callback_wrapper,
            read_concern=ReadConcern(level="local"),
            write_concern=WriteConcern(w=1, j=False)
        )
    except PyMongoError as e:
        print(f"Transazione fallita: {e.args[0]}")

client1.close()
from datetime import datetime

from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client1 = MongoClient(connection_string)

session1 = client1.start_session()
session1.start_transaction(
    read_concern=ReadConcern(level="local"),
    write_concern=WriteConcern(w=1, j=False),
)
db = client1["negozio_abbigliamento"]
capiCollection = db["capi_abbigliamento"]
scontriniCollection = db["scontrini"]

capi = ["Cappotto"]
taglie = ["M"]

articoli = []
totale_complessivo = 0

try:
    print("")
    for capo, taglia in zip(capi, taglie):
        articolo = capiCollection.find_one({'nome': capo}, {'_id': False}, session=session1)
        prezzo_articolo = articolo.get("prezzo").to_decimal()

        print(f"Tentativo di acquisto di {articolo.get('nome')} (taglia: {taglia}) con ID {articolo.get('capoId')}")
        print(articolo)

        time.sleep(3)

        capiCollection.update_one({'nome': capo}, {'$inc': {f'disponibilita.{taglia}': -1}}, session=session1)
        articolo_aggiornato = capiCollection.find_one({'nome': capo}, {'_id': False}, session=session1)
        print(f"Aggiornamento quantità: {articolo_aggiornato}\n")

        articoli.append(
            {"nome": capo, "quantita": 1, "prezzo_totale": Decimal128(str(prezzo_articolo)), "taglia": taglia})
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
    session1.commit_transaction()
    print("Transazione andata a buon fine.\n")
    time.sleep(3)

except Exception as e:
    print(f"\n\nErrore durante la transazione: {e.args[0]}")
    session1.abort_transaction()
    print("\n\nTransazione abortita. \n")

session1.end_session()
client1.close()
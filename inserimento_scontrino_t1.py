from datetime import datetime

from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

# Connessione al client MongoDB
client = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

# Inizio della sessione con transazione
session1 = client.start_session()
session1.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern("majority"),
)

try:
    # Selezione del database e della collezione
    db = client['negozio_abbigliamento']
    capi_abbigliamento = db['capi_abbigliamento']
    scontrini = db['scontrini']

    # Lettura dei prezzi degli articoli
    cappotto = capi_abbigliamento.find_one({'nome': 'Cappotto'}, session=session1)
    prezzo_cappotto = cappotto.get("prezzo")
    quantita_cappotto = cappotto.get("quantita")

    print("T1 - Tentativo di acquisto di " + cappotto.get("nome") + " con ID " + str(cappotto.get("_id")))
    print(cappotto)

    print("")

    time.sleep(3)

    capi_abbigliamento.update_one({'nome': 'Cappotto'}, {'$set': {'quantita': quantita_cappotto - 1}}, session=session1)
    cappotto = capi_abbigliamento.find_one({'nome': 'Cappotto'}, session=session1)
    print(cappotto)

    nuovo_scontrino = {
        "data": datetime.strptime("2024-07-21", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Cappotto", "quantita": 1, "prezzo_totale": prezzo_cappotto}
        ],
        "totale_complessivo": prezzo_cappotto
    }
    scontrini.insert_one(nuovo_scontrino)

    print("T1 - Acquisto terminato")

    print("")

    time.sleep(4)
    session1.commit_transaction()
    print("T1 - Commit")
    print("")
    time.sleep(3)
except Exception as e:
    print(f"Errore durante l'aggiornamento: {e}")
    print("T1 - Abort")
finally:
    session1.end_session()
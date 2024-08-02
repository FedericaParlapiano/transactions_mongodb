from datetime import datetime

from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

# Connessione al client MongoDB
client = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

# Inizio della sessione con transazione
session2 = client.start_session()
session2.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern("majority"),
)

try:
    # Selezione del database e della collezione
    db = client['negozio_abbigliamento']
    capi_abbigliamento = db['capi_abbigliamento']
    scontrini = db['scontrini']

    # Lettura dei prezzi degli articoli
    cappotto = capi_abbigliamento.find_one({'nome': 'Cappotto'}, session=session2)
    jeans = capi_abbigliamento.find_one({'nome': 'Jeans'}, session=session2)
    prezzo_cappotto = cappotto.get("prezzo")
    prezzo_jeans = jeans.get("prezzo")

    print("T2 - Tentativo di acquisto di " + jeans.get("nome") + " con ID " + str(jeans.get("_id")))
    print(jeans)
    print("T2 - Tentativo di acquisto di " + cappotto.get("nome") + " con ID " + str(cappotto.get("_id")))
    print(cappotto)

    print("")

    time.sleep(7)

    capi_abbigliamento.update_one({'nome': 'Jeans'}, {'$inc': {'quantita': - 1}}, session=session2)
    jeans = capi_abbigliamento.find_one({'nome': 'Jeans'}, session=session2)
    print(jeans)
    capi_abbigliamento.update_one({'nome': 'Cappotto'}, {'$inc': {'quantita': - 1}}, session=session2)
    cappotto = capi_abbigliamento.find_one({'nome': 'Cappotto'}, session=session2)
    print(cappotto)


    nuovo_scontrino = {
        "data": datetime.strptime("2024-07-21", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Cappotto", "quantita": 1, "prezzo_totale": prezzo_cappotto},
            {"nome": "Jeans", "quantita": 1, "prezzo_totale": prezzo_jeans}
        ],
        "totale_complessivo": prezzo_cappotto+prezzo_jeans
    }
    scontrini.insert_one(nuovo_scontrino)

    print("T2 - Acquisto terminato")

    print("")

    time.sleep(4)
    session2.commit_transaction()
    print("T2 - Commit")
    print("")
    time.sleep(3)
except Exception as e:
    print(f"Errore durante l'aggiornamento: {e}")
    print("T2 - Abort")
finally:
    session2.end_session()

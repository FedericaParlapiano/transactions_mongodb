from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

# Connessione al client MongoDB
client = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

# Inizio della sessione con transazione
session2 = client.start_session()
session2.start_transaction(
    read_concern=ReadConcern("snapshot"),
    write_concern=WriteConcern("majority"),
)

try:
    # Selezione del database e della collezione
    db = client['negozio_abbigliamento']
    myCollection = db['capi_abbigliamento']

    abito = myCollection.find_one({'nome': 'Abito'}, session=session2)
    prezzo_abito = abito.get("prezzo")

    giacca = myCollection.find_one({'nome': 'Giacca'}, session=session2)
    prezzo_giacca = giacca.get("prezzo")
    pantaloni = myCollection.find_one({'nome': 'Pantaloni'}, session=session2)
    prezzo_pantaloni = pantaloni.get("prezzo")

    prezzo_completo = prezzo_giacca + prezzo_pantaloni

    print("T2 - Prezzo giacca prima dell'update: ", prezzo_giacca)
    print("T2 - Prezzo pantaloni prima dell'update: ", prezzo_pantaloni)
    print("T2 - Prezzo completo giacca e pantaloni: ", round(float(prezzo_completo), 2))
    print("T2 - Prezzo abito: ", prezzo_abito)
    print("")

    # Verifica della condizione e aggiornamento del prezzo
    if prezzo_completo >= prezzo_abito + 20:

        time.sleep(4)
        myCollection.update_one({'nome': 'Pantaloni'}, {'$set': {'prezzo': round(float(prezzo_pantaloni)-40, 2)}}, session=session2)

        pantaloni = myCollection.find_one({'nome': 'Pantaloni'}, session=session2)
        prezzo_pantaloni = pantaloni.get("prezzo")

        print("T2 - Prezzo pantaloni dopo l'update: ", prezzo_pantaloni)
        print("")

        myCollection.update_one({'nome': 'Giacca'}, {'$set': {'prezzo': round(float(prezzo_giacca) + 40, 2)}},
                                session=session2)

        giacca = myCollection.find_one({'nome': 'Giacca'}, session=session2)
        prezzo_giacca = giacca.get("prezzo")
        print("T2 - Prezzo giacca dopo l'update: ", prezzo_giacca)
        print("")

        session2.commit_transaction()
        print("T2 - Commit")
        print("")
    else:
        session2.abort_transaction()
        print("T2 - Abort: il prezzo del completo deve superare quello dell'abito")
        print("")
finally:
    session2.end_session()

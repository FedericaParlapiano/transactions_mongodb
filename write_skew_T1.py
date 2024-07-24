from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

# Connessione al client MongoDB
client = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

# Inizio della sessione con transazione
session1 = client.start_session()
session1.start_transaction(
    read_concern=ReadConcern("snapshot"),
    write_concern=WriteConcern("majority"),
)

try:
    # Selezione del database e della collezione
    db = client['negozio_abbigliamento']
    myCollection = db['capi_abbigliamento']

    # myCollection.update_one({'nome': 'Giacca'}, {'$set': {'prezzo': 89.99}}, session=session1)

    # Lettura dei prezzi degli articoli
    abito = myCollection.find_one({'nome': 'Abito'}, session=session1)
    prezzo_abito = abito.get("prezzo")

    giacca = myCollection.find_one({'nome': 'Giacca'}, session=session1)
    prezzo_giacca = giacca.get("prezzo")
    pantaloni = myCollection.find_one({'nome': 'Pantaloni'}, session=session1)
    prezzo_pantaloni = pantaloni.get("prezzo")

    prezzo_completo = prezzo_giacca + prezzo_pantaloni

    print("T1 - Prezzo giacca prima dell'update: ", prezzo_giacca)
    print("T1 - Prezzo pantaloni prima dell'update: ", prezzo_pantaloni)
    print("T1 - Prezzo completo giacca e pantaloni prima dell'update: ", round(float(prezzo_completo), 2))
    print("T1 - Prezzo abito prima dell'update: ", prezzo_abito)
    print("")

    # Verifica della condizione e aggiornamento del prezzo
    if prezzo_completo >= prezzo_abito + 20:
        myCollection.update_one({'nome': 'Giacca'}, {'$set': {'prezzo': round(float(prezzo_giacca)-20, 2)}}, session=session1)

        giacca = myCollection.find_one({'nome': 'Giacca'}, session=session1)
        prezzo_giacca = giacca.get("prezzo")
        pantaloni = myCollection.find_one({'nome': 'Pantaloni'}, session=session1)
        prezzo_pantaloni = pantaloni.get("prezzo")
        prezzo_completo = prezzo_giacca + prezzo_pantaloni

        abito = myCollection.find_one({'nome': 'Abito'}, session=session1)
        prezzo_abito = abito.get("prezzo")

        print("T1 - Prezzo giacca dopo l'update: ", prezzo_giacca)
        print("T1 - Prezzo pantaloni dopo l'update: ", prezzo_pantaloni)
        print("T1 - Prezzo completo giacca e pantaloni dopo l'update: ", round(float(prezzo_completo), 2))
        print("T1 - Prezzo abito dopo l'update: ", prezzo_abito)
        time.sleep(3)
        session1.commit_transaction()
        print("T1 - Commit")
        print("")
        time.sleep(3)
    else:
        session1.abort_transaction()
        print("T1 - Abort: il prezzo del completo deve superare quello dell'abito di almeno 20 euro")
        print("")
finally:
    session1.end_session()

giacca = myCollection.find_one({'nome': 'Giacca'})
prezzo_giacca = giacca.get("prezzo")
pantaloni = myCollection.find_one({'nome': 'Pantaloni'})
prezzo_pantaloni = pantaloni.get("prezzo")
prezzo_completo = prezzo_giacca + prezzo_pantaloni
abito = myCollection.find_one({'nome': 'Abito'})
prezzo_abito = abito.get("prezzo")

print("T1 - Prezzo giacca dopo il commit: ", round(float(prezzo_giacca), 2))
print("T1 - Prezzo pantaloni dopo il commit: ", round(float(prezzo_pantaloni), 2))
print("T1 - Prezzo abito dopo il commit: ", round(float(prezzo_abito), 2))
print("T1 - Prezzo completo giacca e pantaloni dopo il commit: ", round(float(prezzo_completo), 2))

if prezzo_completo >= prezzo_abito:
    print("Il vincolo è rispettato")
else:
    print("Attenzione! Il vincolo non è rispettato")





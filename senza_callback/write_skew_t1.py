from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

connection_string = "..."
client1 = MongoClient(connection_string)

session1 = client1.start_session()
session1.start_transaction(
    read_concern=ReadConcern(level="local"),
    write_concern=WriteConcern(w=1, j=False),
)

db = client1['negozio_abbigliamento']
capiCollection = db['capi_abbigliamento']

try:
    abito = capiCollection.find_one({'nome': 'Abito'}, session=session1)
    prezzo_abito = abito.get("prezzo").to_decimal()

    giacca = capiCollection.find_one({'nome': 'Giacca'}, session=session1)
    prezzo_giacca = giacca.get("prezzo").to_decimal()
    pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, session=session1)
    prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()

    prezzo_completo = prezzo_giacca + prezzo_pantaloni

    print("Prezzo giacca prima dell'update: ", prezzo_giacca)
    print("Prezzo pantaloni prima dell'update: ", prezzo_pantaloni)
    print("Prezzo completo giacca e pantaloni prima dell'update: ", prezzo_completo)
    print("Prezzo abito prima dell'update: ", prezzo_abito)
    print("")

    # Verifica della condizione e aggiornamento del prezzo
    if prezzo_completo >= prezzo_abito + 20:
        capiCollection.update_one({'nome': 'Giacca'}, {'$set': {'prezzo': Decimal128(str(prezzo_giacca - 20))}},
                                  session=session1)

        giacca = capiCollection.find_one({'nome': 'Giacca'}, session=session1)
        prezzo_giacca = giacca.get("prezzo").to_decimal()
        pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, session=session1)
        prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()
        prezzo_completo = prezzo_giacca + prezzo_pantaloni

        abito = capiCollection.find_one({'nome': 'Abito'}, session=session1)
        prezzo_abito = abito.get("prezzo").to_decimal()

        print("Prezzo giacca dopo l'update: ", prezzo_giacca)
        print("Prezzo pantaloni dopo l'update: ", prezzo_pantaloni)
        print("Prezzo completo giacca e pantaloni dopo l'update: ", prezzo_completo)
        print("Prezzo abito dopo l'update: ", prezzo_abito)
        time.sleep(3)
        session1.commit_transaction()
        print("\nTransazione andata a buon fine.\n")
        time.sleep(3)

        giacca = capiCollection.find_one({'nome': 'Giacca'})
        prezzo_giacca = giacca.get("prezzo").to_decimal()
        pantaloni = capiCollection.find_one({'nome': 'Pantaloni'})
        prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()
        prezzo_completo = prezzo_giacca + prezzo_pantaloni
        abito = capiCollection.find_one({'nome': 'Abito'})
        prezzo_abito = abito.get("prezzo").to_decimal()

        print("Prezzo giacca dopo il commit: ", prezzo_giacca)
        print("Prezzo pantaloni dopo il commit: ", prezzo_pantaloni)
        print("Prezzo cappotto dopo il commit: ", prezzo_abito)
        print("Prezzo completo giacca e pantaloni dopo il commit: ", prezzo_completo)

        if prezzo_completo >= prezzo_abito:
            print("Il vincolo è rispettato")
        else:
            print("Attenzione! Il vincolo non è rispettato")
    else:
        session1.abort_transaction()
        print("Abort: il prezzo del completo deve superare quello dell'abito.\n")
        print("")

except Exception as e:
    print(f"Errore durante la transazione: {e.args[0]}")
    session1.abort_transaction()

finally:
    session1.end_session()
    client1.close()


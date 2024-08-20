from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

connection_string = "..."
client2 = MongoClient(connection_string)

session2 = client2.start_session()
session2.start_transaction(
    read_concern=ReadConcern(level="local"),
    write_concern=WriteConcern(w=1, j=False),
)

db = client2['negozio_abbigliamento']
capiCollection = db['capi_abbigliamento']

try:
    abito = capiCollection.find_one({'nome': 'Abito'}, {'_id': False}, session=session2)
    prezzo_abito = abito.get("prezzo").to_decimal()

    pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, {'_id': False}, session=session2)
    prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()

    giacca = capiCollection.find_one({'nome': 'Giacca'}, {'_id': False}, session=session2)
    prezzo_giacca = giacca.get("prezzo").to_decimal()

    prezzo_completo = prezzo_giacca + prezzo_pantaloni

    print("T2 - Prezzo giacca prima dell'update: ", prezzo_giacca)
    print("T2 - Prezzo pantaloni prima dell'update: ", prezzo_pantaloni)
    print("T2 - Prezzo completo giacca e pantaloni: ", round(float(prezzo_completo), 2))
    print("T2 - Prezzo abito: ", prezzo_abito)
    print("")

    # Verifica della condizione e aggiornamento del prezzo
    if prezzo_completo >= prezzo_abito + 20:

        time.sleep(4)
        capiCollection.update_one({'nome': 'Pantaloni'}, {'$set': {'prezzo': Decimal128(prezzo_pantaloni - 40)}}, session=session2)

        capiCollection.update_one({'nome': 'Giacca'}, {'$set': {'prezzo': Decimal128(prezzo_giacca + 40)}}, session= session2)

        pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, {'_id': False}, session=session2)
        prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()
        print("T2 - Prezzo pantaloni dopo l'update: ", prezzo_pantaloni)
        print("")

        capiCollection.update_one({'nome': 'Giacca'}, {'$set': {'prezzo': Decimal128(prezzo_giacca+40)}},
                                session=session2)

        giacca = capiCollection.find_one({'nome': 'Giacca'}, {'_id': False}, session=session2)
        prezzo_giacca = giacca.get("prezzo").to_decimal()
        print("T2 - Prezzo giacca dopo l'update: ", prezzo_giacca)
        print("")

        session2.commit_transaction()
        print("T2 - Commit")
        print("")
    else:
        session2.abort_transaction()
        print("T2 - Abort: il prezzo del completo deve superare quello dell'cappotto")
        print("")
except Exception as e:
    print(f"Errore durante la transazione: {e.args[0]}")
    session2.abort_transaction()
finally:
    session2.end_session()
    client2.close()

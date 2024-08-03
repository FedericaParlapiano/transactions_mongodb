from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client2 = MongoClient(connection_string)

session2 = client2.start_session()
session2.start_transaction(
    read_concern=ReadConcern("local"),
    write_concern=WriteConcern(w=1, j=False),
)

db = client2['negozio_abbigliamento']
capiCollection = db['capi_abbigliamento']

try:

    abito = capiCollection.find_one({'nome': 'Abito'}, session=session2)
    prezzo_abito = abito.get("prezzo").to_decimal()

    giacca = capiCollection.find_one({'nome': 'Giacca'}, session=session2)
    prezzo_giacca = giacca.get("prezzo").to_decimal()
    pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, session=session2)
    prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()

    prezzo_completo = prezzo_giacca + prezzo_pantaloni

    print("Prezzo giacca prima dell'update: ", prezzo_giacca)
    print("Prezzo pantaloni prima dell'update: ", prezzo_pantaloni)
    print("Prezzo completo giacca e pantaloni prima dell'update: ", prezzo_completo)
    print("Prezzo abito: ", prezzo_abito)
    print("")

    if prezzo_completo >= prezzo_abito + 20:
        capiCollection.update_one({'nome': 'Pantaloni'}, {'$set': {'prezzo': Decimal128(str(prezzo_pantaloni - 20))}},
                                  session=session2)

        pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, {'_id':False}, session=session2)
        prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()
        giacca = capiCollection.find_one({'nome': 'Giacca'}, {'_id':False}, session=session2)
        prezzo_giacca = giacca.get("prezzo").to_decimal()
        prezzo_completo = prezzo_giacca + prezzo_pantaloni

        abito = capiCollection.find_one({'nome': 'Abito'}, {'_id':False}, session=session2)
        prezzo_abito = abito.get("prezzo").to_decimal()

        print("Prezzo giacca dopo l'update: ", prezzo_giacca)
        print("Prezzo pantaloni dopo l'update: ", prezzo_pantaloni)
        print("Prezzo completo giacca e pantaloni dopo l'update: ", prezzo_completo)
        print("Prezzo abito dopo l'update: ", prezzo_abito)
        session2.commit_transaction()
        print("\nTransazione andata a buon fine.\n")
        time.sleep(3)

        giacca = capiCollection.find_one({'nome': 'Giacca'}, {'_id': False})
        prezzo_giacca = giacca.get("prezzo").to_decimal()
        pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, {'_id': False})
        prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()
        prezzo_completo = prezzo_giacca + prezzo_pantaloni
        abito = capiCollection.find_one({'nome': 'Abito'}, {'_id': False})
        prezzo_abito = abito.get("prezzo").to_decimal()

        print("Prezzo giacca dopo il commit: ", round(float(prezzo_giacca), 2))
        print("Prezzo pantaloni dopo il commit: ", round(float(prezzo_pantaloni), 2))
        print("Prezzo abito dopo il commit: ", round(float(prezzo_abito), 2))
        print("Prezzo completo giacca e pantaloni dopo il commit: ", round(float(prezzo_completo), 2))

        if prezzo_completo >= prezzo_abito:
            print("Il vincolo è rispettato")
        else:
            print("Attenzione! Il vincolo non è rispettato.")
    else:
        session2.abort_transaction()
        print("Abort: il prezzo del completo deve superare quello dell'abito.\n")
        print("")

except Exception as e:
    print(f"Errore durante la transazione: {e.args[0]}")
    session2.abort_transaction()

finally:
    session2.end_session()
    client2.close()


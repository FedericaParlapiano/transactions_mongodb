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

    giacca = capiCollection.find_one({'nome': 'Giacca'}, {'_id':False}, session=session1)
    prezzo_giacca = giacca.get("prezzo").to_decimal()

    print("T1 - Prezzo giacca (prima della modifica di T2): ", prezzo_giacca)
    print("")

    time.sleep(6)

    abito = capiCollection.find_one({'nome': 'Abito'}, {'_id':False}, session=session1)
    prezzo_abito = abito.get("prezzo").to_decimal()

    pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, {'_id':False}, session=session1)
    prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()

    prezzo_completo = prezzo_giacca + prezzo_pantaloni

    print("T1 - Prezzo pantaloni (dopo le modifiche di T2): ", prezzo_pantaloni)
    print("\nT1 - Prezzo completo giacca e pantaloni (dopo le modifiche di T2): ", round(float(prezzo_completo), 2))
    print("T1 - Prezzo abito: ", prezzo_abito)
    print("")

    if prezzo_completo >= prezzo_abito:
        print("T1 - Vincolo soddisfatto")
    else:
        session1.abort_transaction()
        print("T1 - Vincolo non soddisfatto")
        print("Transazione abortita.")

except Exception as e:
    print(f"Errore durante la transazione: {e.args[0]}")
    session1.abort_transaction()

finally:
    session1.end_session()
    client1.close()





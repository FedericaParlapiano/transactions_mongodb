from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

client = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

session1 = client.start_session()
session1.start_transaction(
    read_concern=ReadConcern("snapshot"),
    write_concern=WriteConcern("majority"),
)

try:

    db = client['negozio_abbigliamento']
    myCollection = db['capi_abbigliamento']

    giacca = myCollection.find_one({'nome': 'Giacca'}, session=session1)
    prezzo_giacca = giacca.get("prezzo")

    print("T1 - Prezzo giacca (prima della modifica di T2): ", prezzo_giacca)
    print("")

    time.sleep(6)

    abito = myCollection.find_one({'nome': 'Abito'}, session=session1)
    prezzo_abito = abito.get("prezzo")

    pantaloni = myCollection.find_one({'nome': 'Pantaloni'}, session=session1)
    prezzo_pantaloni = pantaloni.get("prezzo")

    prezzo_completo = prezzo_giacca + prezzo_pantaloni

    print("T1 - Prezzo pantaloni (dopo le modifiche di T2): ", prezzo_pantaloni)
    print("T1 - Prezzo completo giacca e pantaloni (dopo le modifiche di T2): ", round(float(prezzo_completo), 2))
    print("T1 - Prezzo abito: ", prezzo_abito)
    print("")

    if prezzo_completo >= prezzo_abito:
        print("T1 - Vincolo soddisfatto")
    else:
        session1.abort_transaction()
        print("T1 - Vincolo non soddisfatto")

finally:
    session1.end_session()





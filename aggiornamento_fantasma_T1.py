from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from pymongo.read_concern import ReadConcern
import time

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client = MongoClient(connection_string)

def callback(session):
    capiCollection = session.client.negozio_abbigliamento.capi_abbigliamento.with_options(
        write_concern=WriteConcern(w=1, j=False)
    )


    try:

        giacca = capiCollection.find_one({'nome': 'Giacca'}, session=session)
        prezzo_giacca = giacca.get("prezzo").to_decimal()

        print("T1 - Prezzo giacca (prima della modifica di T2): ", prezzo_giacca)
        print("\n\n\n")

        time.sleep(7)

        abito = capiCollection.find_one({'nome': 'Abito'}, session=session)
        prezzo_abito = abito.get("prezzo").to_decimal()

        pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, session=session)
        prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()

        prezzo_completo = prezzo_giacca + prezzo_pantaloni

        print("T1 - Prezzo pantaloni (dopo le modifiche di T2): ", prezzo_pantaloni)
        print("T1 - Prezzo completo giacca e pantaloni (dopo le modifiche di T2): ", Decimal128(prezzo_completo))
        print("T1 - Prezzo cappotto: ", prezzo_abito)
        print("")

        if prezzo_completo >= prezzo_abito:
            print("T1 - Vincolo soddisfatto")
        else:
            session.abort_transaction()
            print("T1 - Vincolo non soddisfatto")

    finally:
        session.end_session()


def callback_wrapper(s):
    callback(
        session=s
    )


with client.start_session() as session:
    try:
        session.with_transaction(
            callback_wrapper,
            read_concern=ReadConcern(level="local"),
            write_concern=WriteConcern(w=1, j=False)
        )
    except PyMongoError as e:
        print(f"Transazione fallita: {e.args[0]}")

client.close()


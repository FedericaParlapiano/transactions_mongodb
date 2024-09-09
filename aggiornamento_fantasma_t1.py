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
        read_concern=ReadConcern(level="local"),
        write_concern=WriteConcern(w=1, j=False)
    )

    try:

        giacca = capiCollection.find_one({'nome': 'Giacca'}, {'_id':False}, session=session)
        prezzo_giacca = giacca.get("prezzo").to_decimal()

        print("Prezzo giacca (prima della modifica di T2): ", prezzo_giacca)
        print("\n\n")

        time.sleep(5)

        abito = capiCollection.find_one({'nome': 'Abito'}, {'_id':False}, session=session)
        prezzo_abito = abito.get("prezzo").to_decimal()

        pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, {'_id':False}, session=session)
        prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()

        prezzo_completo = prezzo_giacca + prezzo_pantaloni

        print("Prezzo pantaloni (dopo le modifiche di T2): ", prezzo_pantaloni)
        print("\nPrezzo completo giacca e pantaloni (dopo le modifiche di T2): ", Decimal128(prezzo_completo))
        print("Prezzo abito: ", prezzo_abito)
        print("")

        if prezzo_completo >= prezzo_abito:
            print("Vincolo soddisfatto")
        else:
            print("Vincolo non soddisfatto")
            print("Transazione abortita.")

    except Exception as e:
        print(f"Errore durante la transazione: {e.args[0]}")

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


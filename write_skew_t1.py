from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from pymongo.read_concern import ReadConcern
import time

connection_string = "..."
client = MongoClient(connection_string)

def callback(session):
    capiCollection = session.client.negozio_abbigliamento.capi_abbigliamento.with_options(
        write_concern=WriteConcern(w=1, j=False)
    )

    try:
        abito = capiCollection.find_one({'nome': 'Abito'}, session=session)
        prezzo_abito = abito.get("prezzo").to_decimal()

        giacca = capiCollection.find_one({'nome': 'Giacca'}, session=session)
        prezzo_giacca = giacca.get("prezzo").to_decimal()
        pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, session=session)
        prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()

        prezzo_completo = prezzo_giacca + prezzo_pantaloni

        print("Prezzo giacca prima dell'update: ", prezzo_giacca)
        print("Prezzo pantaloni prima dell'update: ", prezzo_pantaloni)
        print("Prezzo completo giacca e pantaloni prima dell'update: ", prezzo_completo)
        print("Prezzo abito prima dell'update: ", prezzo_abito)
        print("")
        time.sleep(3)

        if prezzo_completo >= prezzo_abito + 20:
            capiCollection.update_one({'nome': 'Pantaloni'}, {'$set': {'lock': 'true'}}, session=session)
            capiCollection.update_one({'nome': 'Giacca'}, {'$set': {'prezzo': Decimal128(str(prezzo_giacca-20))}}, session=session)

            giacca = capiCollection.find_one({'nome': 'Giacca'}, session=session)
            prezzo_giacca = giacca.get("prezzo").to_decimal()
            pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, session=session)
            prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()
            prezzo_completo = prezzo_giacca + prezzo_pantaloni

            abito = capiCollection.find_one({'nome': 'Abito'}, session=session)
            prezzo_abito = abito.get("prezzo").to_decimal()

            print("Prezzo giacca dopo l'update: ", prezzo_giacca)
            print("Prezzo pantaloni dopo l'update: ", prezzo_pantaloni)
            print("Prezzo completo giacca e pantaloni dopo l'update: ", prezzo_completo)
            print("Prezzo abito dopo l'update: ", prezzo_abito)
            time.sleep(3)

            capiCollection.update_one({'nome': 'Pantaloni'}, {'$unset': {'lock': 1}}, session=session)
            session.commit_transaction()
            print("\nTransazione andata a buon fine.\n")
            time.sleep(3)
        else:
            session.abort_transaction()
            print("Abort: il prezzo del completo deve superare quello dell'abito.\n")
            return
    except Exception as e:
        print(f"Errore durante la transazione: {e.args[0]}")
        session.abort_transaction()
        return
    finally:
        session.end_session()

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

